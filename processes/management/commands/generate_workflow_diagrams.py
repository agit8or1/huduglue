"""
Management command to auto-generate flowchart diagrams from workflows.

Usage:
    python manage.py generate_workflow_diagrams
    python manage.py generate_workflow_diagrams --workflow-id 123
    python manage.py generate_workflow_diagrams --update-existing
"""

from django.core.management.base import BaseCommand
from processes.models import Process, ProcessStage
from docs.models import Diagram
import xml.etree.ElementTree as ET


class Command(BaseCommand):
    help = 'Auto-generate flowchart diagrams from workflow/process steps'

    def add_arguments(self, parser):
        parser.add_argument(
            '--workflow-id',
            type=int,
            help='Specific workflow/process ID to generate diagram for'
        )
        parser.add_argument(
            '--update-existing',
            action='store_true',
            help='Update diagrams for workflows that already have linked diagrams'
        )

    def handle(self, *args, **options):
        workflow_id = options.get('workflow_id')
        update_existing = options.get('update_existing', False)

        self.stdout.write(self.style.SUCCESS('Generating workflow flowchart diagrams...'))

        # Get workflows to process
        workflows = Process.objects.all()

        if workflow_id:
            workflows = workflows.filter(id=workflow_id)
            if not workflows.exists():
                self.stdout.write(self.style.ERROR(f'Workflow with ID {workflow_id} not found'))
                return

        if not update_existing:
            workflows = workflows.filter(linked_diagram__isnull=True)

        count = 0
        for workflow in workflows:
            try:
                diagram_xml = self._generate_flowchart_xml(workflow)

                # Create or update diagram
                if workflow.linked_diagram and update_existing:
                    diagram = workflow.linked_diagram
                    diagram.diagram_xml = diagram_xml
                    diagram.description = f'Auto-generated flowchart for {workflow.title}'
                    diagram.save()
                    self.stdout.write(f'  ✓ Updated diagram for: {workflow.title}')
                else:
                    diagram = Diagram.objects.create(
                        organization=workflow.organization,
                        title=f'{workflow.title} - Flowchart',
                        slug=f'{workflow.slug}-flowchart',
                        diagram_type='flowchart',
                        diagram_xml=diagram_xml,
                        description=f'Auto-generated flowchart for {workflow.title}',
                        created_by=workflow.created_by,
                    )
                    workflow.linked_diagram = diagram
                    workflow.save()
                    self.stdout.write(f'  ✓ Generated diagram for: {workflow.title}')

                count += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Failed for {workflow.title}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'\\nGenerated/updated {count} workflow diagrams'))
        self.stdout.write(self.style.WARNING('\\nNote: Open each diagram in the editor and save to generate PNG previews.'))

    def _generate_flowchart_xml(self, workflow):
        """
        Generate draw.io XML for a flowchart based on workflow steps.
        Uses a simple vertical flow with start/end nodes.
        """
        stages = workflow.stages.all().order_by('order')

        # Draw.io XML structure
        # This is a simplified version - a full draw.io XML is quite complex
        xml_template = '''<mxfile host="app.diagrams.net">
  <diagram name="Page-1" id="workflow-{workflow_id}">
    <mxGraphModel dx="800" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        {shapes}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''

        shapes = []
        current_id = 2
        y_position = 60
        x_position = 325
        shape_height = 80
        shape_width = 200
        spacing = 120

        # Start node (rounded rectangle/ellipse)
        shapes.append(f'''
        <mxCell id="{current_id}" value="Start: {workflow.title[:30]}" style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="{x_position}" y="{y_position}" width="{shape_width}" height="60" as="geometry" />
        </mxCell>''')
        prev_id = current_id
        current_id += 1
        y_position += 60 + spacing

        # Process stages
        for idx, stage in enumerate(stages):
            # Stage box
            fill_color = "#dae8fc" if idx % 2 == 0 else "#fff2cc"
            stroke_color = "#6c8ebf" if idx % 2 == 0 else "#d6b656"

            stage_label = stage.title[:40]
            if stage.requires_confirmation:
                # Diamond for decision points
                shapes.append(f'''
        <mxCell id="{current_id}" value="{stage_label}?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff3cd;strokeColor=#ffc107;" vertex="1" parent="1">
          <mxGeometry x="{x_position - 50}" y="{y_position}" width="{shape_width + 100}" height="{shape_height + 20}" as="geometry" />
        </mxCell>''')
                y_offset = shape_height + 20
            else:
                # Rectangle for standard steps
                shapes.append(f'''
        <mxCell id="{current_id}" value="{stage_label}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill_color};strokeColor={stroke_color};" vertex="1" parent="1">
          <mxGeometry x="{x_position}" y="{y_position}" width="{shape_width}" height="{shape_height}" as="geometry" />
        </mxCell>''')
                y_offset = shape_height

            # Connection from previous
            shapes.append(f'''
        <mxCell id="{current_id + 1}" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;endFill=1;" edge="1" parent="1" source="{prev_id}" target="{current_id}">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>''')

            prev_id = current_id
            current_id += 2
            y_position += y_offset + spacing

        # End node
        shapes.append(f'''
        <mxCell id="{current_id}" value="End" style="ellipse;whiteSpace=wrap;html=1;fillColor=#f8d7da;strokeColor=#dc3545;" vertex="1" parent="1">
          <mxGeometry x="{x_position}" y="{y_position}" width="{shape_width}" height="60" as="geometry" />
        </mxCell>''')

        # Final connection
        shapes.append(f'''
        <mxCell id="{current_id + 1}" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;endFill=1;" edge="1" parent="1" source="{prev_id}" target="{current_id}">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>''')

        # Build final XML
        diagram_xml = xml_template.format(
            workflow_id=workflow.id,
            shapes=''.join(shapes)
        )

        return diagram_xml
