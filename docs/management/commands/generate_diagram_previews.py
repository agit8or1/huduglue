"""
Management command to generate preview images for diagram templates using PIL.

Usage:
    python manage.py generate_diagram_previews
    python manage.py generate_diagram_previews --force
"""

from django.core.management.base import BaseCommand
from docs.models import Diagram
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile
import textwrap


class Command(BaseCommand):
    help = 'Generate preview images for diagram templates using PIL'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Regenerate previews even if they already exist',
        )

    def handle(self, *args, **options):
        force = options.get('force', False)

        self.stdout.write(self.style.SUCCESS('Generating diagram preview images...'))

        # Get all diagrams
        diagrams = Diagram.objects.all()

        if not force:
            # Only generate for diagrams without PNG exports or thumbnails
            # Use Q objects with isnull and exact='' for FileField empty checks
            from django.db.models import Q
            diagrams = diagrams.filter(
                Q(png_export='') | Q(png_export__isnull=True),
                Q(thumbnail='') | Q(thumbnail__isnull=True)
            )

        count = 0
        for diagram in diagrams:
            try:
                # Generate preview image based on diagram type
                img = self._generate_preview_image(diagram)

                # Save as PNG export
                buffer = BytesIO()
                img.save(buffer, format='PNG', optimize=True)
                buffer.seek(0)

                filename = f"{diagram.slug}.png"
                diagram.png_export.save(filename, ContentFile(buffer.read()), save=False)

                # Generate thumbnail (smaller version)
                thumb_img = img.resize((300, 200), Image.Resampling.LANCZOS)
                thumb_buffer = BytesIO()
                thumb_img.save(thumb_buffer, format='PNG', optimize=True)
                thumb_buffer.seek(0)

                thumb_filename = f"{diagram.slug}_thumb.png"
                diagram.thumbnail.save(thumb_filename, ContentFile(thumb_buffer.read()), save=True)

                self.stdout.write(f'  ✓ Generated preview for: {diagram.title}')
                count += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Failed for {diagram.title}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'\\nGenerated {count} diagram preview images'))

    def _generate_preview_image(self, diagram):
        """Generate a preview image based on diagram type."""
        width, height = 800, 600
        bg_color = '#FFFFFF'

        # Create base image
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)

        # Try to load a font, fall back to default if not available
        try:
            title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 32)
            text_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
            small_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        # Draw based on diagram type
        diagram_type = diagram.diagram_type

        if diagram_type == 'network':
            self._draw_network_diagram(draw, width, height, text_font)
        elif diagram_type == 'rack':
            self._draw_rack_diagram(draw, width, height, text_font)
        elif diagram_type == 'process':
            self._draw_process_diagram(draw, width, height, text_font)
        elif diagram_type == 'architecture':
            self._draw_architecture_diagram(draw, width, height, text_font)
        elif diagram_type == 'floorplan':
            self._draw_floorplan_diagram(draw, width, height, text_font)
        elif diagram_type == 'org':
            self._draw_org_diagram(draw, width, height, text_font)
        elif diagram_type == 'erd':
            self._draw_erd_diagram(draw, width, height, text_font)
        elif diagram_type == 'flowchart':
            self._draw_flowchart_diagram(draw, width, height, text_font)
        else:
            self._draw_generic_diagram(draw, width, height, text_font)

        # Draw title at bottom
        title_text = diagram.title
        if len(title_text) > 40:
            title_text = title_text[:37] + '...'

        # Draw title background
        bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = bbox[2] - bbox[0]
        title_height = bbox[3] - bbox[1]
        title_x = (width - title_width) // 2
        title_y = height - title_height - 40

        draw.rectangle([0, height - 80, width, height], fill='#0d6efd')
        draw.text((title_x, title_y), title_text, fill='#FFFFFF', font=title_font)

        return img

    def _draw_network_diagram(self, draw, width, height, font):
        """Draw a network topology representation."""
        # Cloud (Internet)
        draw.ellipse([width//2 - 60, 80, width//2 + 60, 140], outline='#6c8ebf', fill='#dae8fc', width=3)
        draw.text((width//2 - 30, 100), "Internet", fill='#000000', font=font)

        # Firewall
        draw.rectangle([width//2 - 60, 180, width//2 + 60, 230], outline='#b85450', fill='#f8cecc', width=3)
        draw.text((width//2 - 35, 195), "Firewall", fill='#000000', font=font)

        # Switch
        draw.rectangle([width//2 - 60, 270, width//2 + 60, 320], outline='#d6b656', fill='#fff2cc', width=3)
        draw.text((width//2 - 30, 285), "Switch", fill='#000000', font=font)

        # Servers
        for i, label in enumerate(['Web', 'App', 'DB']):
            x = width//2 - 150 + i * 150
            draw.rectangle([x - 40, 380, x + 40, 430], outline='#82b366', fill='#d5e8d4', width=2)
            draw.text((x - 20, 395), label, fill='#000000', font=font)

        # Connections
        draw.line([width//2, 140, width//2, 180], fill='#000000', width=2)
        draw.line([width//2, 230, width//2, 270], fill='#000000', width=2)
        for i in range(3):
            x = width//2 - 150 + i * 150
            draw.line([width//2, 320, x, 380], fill='#000000', width=2)

    def _draw_rack_diagram(self, draw, width, height, font):
        """Draw a server rack representation."""
        rack_x = width // 2 - 100
        rack_y = 100
        rack_width = 200
        rack_height = 400

        # Rack frame
        draw.rectangle([rack_x, rack_y, rack_x + rack_width, rack_y + rack_height],
                      outline='#000000', fill='#2f2f2f', width=4)

        # Rack units
        colors = ['#0d6efd', '#6c757d', '#198754', '#ffc107', '#dc3545']
        labels = ['Switch', 'Server 1', 'Server 2', 'Server 3', 'PDU']

        unit_height = 35
        for i in range(5):
            y = rack_y + 50 + i * (unit_height + 10)
            draw.rectangle([rack_x + 10, y, rack_x + rack_width - 10, y + unit_height],
                          outline='#000000', fill=colors[i], width=2)
            draw.text((rack_x + 40, y + 8), labels[i], fill='#FFFFFF', font=font)

    def _draw_process_diagram(self, draw, width, height, font):
        """Draw a process flowchart representation."""
        # Start
        draw.ellipse([width//2 - 60, 100, width//2 + 60, 160], outline='#82b366', fill='#d5e8d4', width=3)
        draw.text((width//2 - 20, 120), "Start", fill='#000000', font=font)

        # Process steps
        steps = ['Process 1', 'Process 2', 'Process 3']
        for i, step in enumerate(steps):
            y = 210 + i * 100
            draw.rectangle([width//2 - 80, y, width//2 + 80, y + 50],
                          outline='#0d6efd', fill='#cfe2ff', width=3)
            draw.text((width//2 - 40, y + 15), step, fill='#000000', font=font)
            if i < len(steps):
                draw.line([width//2, y + 50, width//2, y + 100], fill='#000000', width=2)

        # End
        draw.ellipse([width//2 - 60, 510, width//2 + 60, 570], outline='#dc3545', fill='#f8d7da', width=3)
        draw.text((width//2 - 15, 530), "End", fill='#000000', font=font)

    def _draw_architecture_diagram(self, draw, width, height, font):
        """Draw a system architecture representation."""
        # Frontend
        draw.rectangle([100, 150, 250, 220], outline='#0d6efd', fill='#cfe2ff', width=3)
        draw.text((130, 175), "Frontend", fill='#000000', font=font)

        # API Gateway
        draw.rectangle([320, 150, 480, 220], outline='#6c757d', fill='#e2e3e5', width=3)
        draw.text((340, 175), "API Gateway", fill='#000000', font=font)

        # Backend Services
        draw.rectangle([550, 100, 680, 170], outline='#198754', fill='#d1e7dd', width=3)
        draw.text((560, 125), "Service 1", fill='#000000', font=font)

        draw.rectangle([550, 200, 680, 270], outline='#198754', fill='#d1e7dd', width=3)
        draw.text((560, 225), "Service 2", fill='#000000', font=font)

        # Database
        draw.ellipse([580, 350, 650, 420], outline='#ffc107', fill='#fff3cd', width=3)
        draw.text((590, 375), "Database", fill='#000000', font=font)

        # Connections
        draw.line([250, 185, 320, 185], fill='#000000', width=2)
        draw.line([480, 165, 550, 135], fill='#000000', width=2)
        draw.line([480, 200, 550, 235], fill='#000000', width=2)
        draw.line([615, 270, 615, 350], fill='#000000', width=2)

    def _draw_floorplan_diagram(self, draw, width, height, font):
        """Draw a floor plan representation."""
        # Rooms
        rooms = [
            {'x': 100, 'y': 100, 'w': 200, 'h': 180, 'label': 'Office 1'},
            {'x': 100, 'y': 320, 'w': 200, 'h': 180, 'label': 'Office 2'},
            {'x': 340, 'y': 100, 'w': 360, 'h': 180, 'label': 'Conference Room'},
            {'x': 340, 'y': 320, 'w': 180, 'h': 180, 'label': 'Server Room'},
            {'x': 560, 'y': 320, 'w': 140, 'h': 180, 'label': 'Storage'},
        ]

        for room in rooms:
            draw.rectangle([room['x'], room['y'], room['x'] + room['w'], room['y'] + room['h']],
                          outline='#000000', fill='#f8f9fa', width=3)
            draw.text((room['x'] + 10, room['y'] + room['h']//2), room['label'],
                     fill='#000000', font=font)

        # Doors
        door_positions = [
            (200, 100), (200, 320), (520, 210), (430, 320)
        ]
        for x, y in door_positions:
            draw.line([x, y, x, y + 30], fill='#000000', width=6)

    def _draw_org_diagram(self, draw, width, height, font):
        """Draw an organizational chart representation."""
        # CEO
        draw.rectangle([width//2 - 60, 80, width//2 + 60, 130],
                      outline='#0d6efd', fill='#cfe2ff', width=3)
        draw.text((width//2 - 20, 95), "CEO", fill='#000000', font=font)

        # Department heads
        positions = [
            (width//2 - 220, 220, "CTO"),
            (width//2 - 60, 220, "CFO"),
            (width//2 + 100, 220, "COO")
        ]

        for x, y, label in positions:
            draw.rectangle([x, y, x + 120, y + 50],
                          outline='#198754', fill='#d1e7dd', width=2)
            draw.text((x + 10, y + 15), label, fill='#000000', font=font)
            draw.line([width//2, 130, x + 60, y], fill='#000000', width=2)

        # Team members under CTO
        for i in range(3):
            x = width//2 - 260 + i * 80
            y = 340
            draw.rectangle([x, y, x + 70, y + 40],
                          outline='#6c757d', fill='#e2e3e5', width=2)
            draw.text((x + 10, y + 12), f"Dev {i+1}", fill='#000000', font=font)
            draw.line([width//2 - 160, 270, x + 35, y], fill='#000000', width=1)

    def _draw_erd_diagram(self, draw, width, height, font):
        """Draw an entity-relationship diagram representation."""
        # Entities
        entities = [
            {'x': 150, 'y': 150, 'label': 'Users'},
            {'x': 400, 'y': 150, 'label': 'Orders'},
            {'x': 650, 'y': 150, 'label': 'Products'},
            {'x': 400, 'y': 350, 'label': 'OrderItems'}
        ]

        for entity in entities:
            draw.rectangle([entity['x'], entity['y'], entity['x'] + 120, entity['y'] + 80],
                          outline='#0d6efd', fill='#cfe2ff', width=3)
            draw.text((entity['x'] + 10, entity['y'] + 10), entity['label'],
                     fill='#000000', font=font)
            # Fields
            draw.line([entity['x'], entity['y'] + 35, entity['x'] + 120, entity['y'] + 35],
                     fill='#0d6efd', width=2)

        # Relationships
        draw.line([270, 190, 400, 190], fill='#000000', width=2)
        draw.text((320, 170), "1:N", fill='#000000', font=font)

        draw.line([520, 190, 650, 190], fill='#000000', width=2)
        draw.text((570, 170), "N:M", fill='#000000', font=font)

        draw.line([460, 230, 460, 350], fill='#000000', width=2)
        draw.text((465, 280), "1:N", fill='#000000', font=font)

    def _draw_flowchart_diagram(self, draw, width, height, font):
        """Draw a flowchart representation."""
        # Start
        draw.ellipse([width//2 - 60, 80, width//2 + 60, 140],
                    outline='#82b366', fill='#d5e8d4', width=3)
        draw.text((width//2 - 20, 100), "Start", fill='#000000', font=font)

        # Decision
        points = [
            (width//2, 200),
            (width//2 + 80, 260),
            (width//2, 320),
            (width//2 - 80, 260)
        ]
        draw.polygon(points, outline='#ffc107', fill='#fff3cd', width=3)
        draw.text((width//2 - 30, 250), "Decision?", fill='#000000', font=font)

        # Yes path
        draw.rectangle([width//2 + 120, 230, width//2 + 240, 290],
                      outline='#198754', fill='#d1e7dd', width=3)
        draw.text((width//2 + 140, 250), "Action A", fill='#000000', font=font)
        draw.line([width//2 + 80, 260, width//2 + 120, 260], fill='#000000', width=2)
        draw.text((width//2 + 85, 240), "Yes", fill='#000000', font=font)

        # No path
        draw.rectangle([width//2 - 240, 230, width//2 - 120, 290],
                      outline='#dc3545', fill='#f8d7da', width=3)
        draw.text((width//2 - 220, 250), "Action B", fill='#000000', font=font)
        draw.line([width//2 - 80, 260, width//2 - 120, 260], fill='#000000', width=2)
        draw.text((width//2 - 110, 240), "No", fill='#000000', font=font)

        # End
        draw.ellipse([width//2 - 60, 380, width//2 + 60, 440],
                    outline='#6c757d', fill='#e2e3e5', width=3)
        draw.text((width//2 - 15, 400), "End", fill='#000000', font=font)

        # Connections
        draw.line([width//2, 140, width//2, 200], fill='#000000', width=2)
        draw.line([width//2 + 180, 290, width//2 + 180, 360, width//2 + 60, 400], fill='#000000', width=2)
        draw.line([width//2 - 180, 290, width//2 - 180, 360, width//2 - 60, 400], fill='#000000', width=2)

    def _draw_generic_diagram(self, draw, width, height, font):
        """Draw a generic diagram representation."""
        # Draw a grid of connected boxes
        for i in range(2):
            for j in range(3):
                x = 150 + j * 200
                y = 180 + i * 180
                draw.rectangle([x, y, x + 140, y + 80],
                             outline='#0d6efd', fill='#cfe2ff', width=3)
                draw.text((x + 30, y + 25), f"Node {i*3+j+1}",
                         fill='#000000', font=font)

                # Draw connections
                if j < 2:
                    draw.line([x + 140, y + 40, x + 200, y + 40],
                             fill='#000000', width=2)
                if i == 0:
                    draw.line([x + 70, y + 80, x + 70, y + 180],
                             fill='#000000', width=2)
