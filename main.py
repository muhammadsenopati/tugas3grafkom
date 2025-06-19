import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import math
import json
import copy

class DrawingObject:
    def __init__(self, obj_type, start_pos, end_pos, color, thickness):
        self.id = id(self)
        self.type = obj_type
        self.start = start_pos
        self.end = end_pos
        self.color = color
        self.thickness = thickness
        self.transform = {
            'translateX': 0,
            'translateY': 0,
            'scale': 1.0,
            'rotation': 0
        }

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Grafis 2D")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f8ff')
        
        # Application state
        self.current_mode = 'draw'
        self.current_tool = 'point'
        self.current_color = '#4299e1'
        self.current_thickness = 3
        self.is_drawing = False
        self.start_pos = None
        self.objects = []
        self.selected_object = None
        self.history = []
        self.history_step = -1
        
        # Canvas variables
        self.canvas_width = 800
        self.canvas_height = 500
        
        self.setup_ui()
        self.setup_bindings()
        self.save_state()
        self.update_status("Siap untuk menggambar")

    def setup_ui(self):
        # Main title
        title_label = tk.Label(self.root, text="Aplikasi Grafis 2D", 
                              font=('Segoe UI', 24, 'normal'), 
                              bg='#f0f8ff', fg='#2d3748')
        title_label.pack(pady=10)

        # Controls frame
        controls_frame = tk.Frame(self.root, bg='#e6f3ff', relief='ridge', bd=2)
        controls_frame.pack(fill='x', padx=10, pady=5)

        # Mode controls
        mode_frame = tk.LabelFrame(controls_frame, text="Mode", 
                                  font=('Segoe UI', 10, 'bold'),
                                  bg='#e6f3ff', fg='#2d3748')
        mode_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.mode_var = tk.StringVar(value='draw')
        tk.Radiobutton(mode_frame, text="Gambar", variable=self.mode_var, 
                      value='draw', command=self.change_mode,
                      bg='#e6f3ff', fg='#4299e1', font=('Segoe UI', 9),
                      selectcolor='#4299e1').pack(side='left', padx=5)
        tk.Radiobutton(mode_frame, text="Pilih", variable=self.mode_var, 
                      value='select', command=self.change_mode,
                      bg='#e6f3ff', fg='#4299e1', font=('Segoe UI', 9),
                      selectcolor='#4299e1').pack(side='left', padx=5)

        # Tool controls
        tool_frame = tk.LabelFrame(controls_frame, text="Alat Gambar", 
                                  font=('Segoe UI', 10, 'bold'),
                                  bg='#e6f3ff', fg='#2d3748')
        tool_frame.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.tool_var = tk.StringVar(value='point')
        tools = [('Titik', 'point'), ('Garis', 'line'), ('Persegi', 'rectangle'), ('Ellipse', 'ellipse')]
        for text, value in tools:
            tk.Radiobutton(tool_frame, text=text, variable=self.tool_var, 
                          value=value, command=self.change_tool,
                          bg='#e6f3ff', fg='#4299e1', font=('Segoe UI', 9),
                          selectcolor='#4299e1').pack(side='left', padx=3)

        # Color and thickness controls
        settings_frame = tk.LabelFrame(controls_frame, text="Pengaturan", 
                                      font=('Segoe UI', 10, 'bold'),
                                      bg='#e6f3ff', fg='#2d3748')
        settings_frame.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        tk.Button(settings_frame, text="Pilih Warna", command=self.choose_color,
                 bg='#4299e1', fg='white', font=('Segoe UI', 9),
                 relief='raised', bd=2).pack(side='left', padx=3)

        tk.Label(settings_frame, text="Ketebalan:", bg='#e6f3ff', 
                fg='#2d3748', font=('Segoe UI', 9)).pack(side='left', padx=3)
        
        self.thickness_var = tk.IntVar(value=3)
        thickness_scale = tk.Scale(settings_frame, from_=1, to=20, 
                                  orient='horizontal', variable=self.thickness_var,
                                  command=self.change_thickness, length=100,
                                  bg='#e6f3ff', fg='#4299e1', font=('Segoe UI', 8))
        thickness_scale.pack(side='left', padx=3)

        # Action controls
        action_frame = tk.LabelFrame(controls_frame, text="Aksi", 
                                    font=('Segoe UI', 10, 'bold'),
                                    bg='#e6f3ff', fg='#2d3748')
        action_frame.grid(row=0, column=3, padx=5, pady=5, sticky='ew')

        self.undo_btn = tk.Button(action_frame, text="Undo", command=self.undo,
                                 bg='#4299e1', fg='white', font=('Segoe UI', 9),
                                 relief='raised', bd=2, state='disabled')
        self.undo_btn.pack(side='left', padx=2)

        self.redo_btn = tk.Button(action_frame, text="Redo", command=self.redo,
                                 bg='#4299e1', fg='white', font=('Segoe UI', 9),
                                 relief='raised', bd=2, state='disabled')
        self.redo_btn.pack(side='left', padx=2)

        # Configure grid weights
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)
        controls_frame.grid_columnconfigure(2, weight=1)
        controls_frame.grid_columnconfigure(3, weight=1)

        # Canvas frame
        canvas_frame = tk.Frame(self.root, bg='#4299e1', relief='ridge', bd=3)
        canvas_frame.pack(padx=10, pady=5)

        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width, 
                               height=self.canvas_height, bg='white',
                               cursor='crosshair')
        self.canvas.pack()

        # Transform controls
        transform_frame = tk.LabelFrame(self.root, text="Transformasi Objek Terpilih", 
                                       font=('Segoe UI', 12, 'bold'),
                                       bg='#f0f8ff', fg='#2d3748')
        transform_frame.pack(fill='x', padx=10, pady=10)

        # Transform inputs
        transform_inputs = tk.Frame(transform_frame, bg='#f0f8ff')
        transform_inputs.pack(fill='x', padx=10, pady=10)

        # Translasi X
        tk.Label(transform_inputs, text="Translasi X:", bg='#f0f8ff', 
                fg='#2d3748', font=('Segoe UI', 9)).grid(row=0, column=0, padx=5, sticky='w')
        self.translate_x_var = tk.StringVar(value='0')
        self.translate_x_entry = tk.Entry(transform_inputs, textvariable=self.translate_x_var,
                                         width=10, state='disabled', font=('Segoe UI', 9))
        self.translate_x_entry.grid(row=0, column=1, padx=5)
        self.translate_x_entry.bind('<KeyRelease>', self.apply_transform)

        # Translasi Y
        tk.Label(transform_inputs, text="Translasi Y:", bg='#f0f8ff', 
                fg='#2d3748', font=('Segoe UI', 9)).grid(row=0, column=2, padx=5, sticky='w')
        self.translate_y_var = tk.StringVar(value='0')
        self.translate_y_entry = tk.Entry(transform_inputs, textvariable=self.translate_y_var,
                                         width=10, state='disabled', font=('Segoe UI', 9))
        self.translate_y_entry.grid(row=0, column=3, padx=5)
        self.translate_y_entry.bind('<KeyRelease>', self.apply_transform)

        # Skala
        tk.Label(transform_inputs, text="Skala:", bg='#f0f8ff', 
                fg='#2d3748', font=('Segoe UI', 9)).grid(row=1, column=0, padx=5, sticky='w')
        self.scale_var = tk.StringVar(value='1.0')
        self.scale_entry = tk.Entry(transform_inputs, textvariable=self.scale_var,
                                   width=10, state='disabled', font=('Segoe UI', 9))
        self.scale_entry.grid(row=1, column=1, padx=5)
        self.scale_entry.bind('<KeyRelease>', self.apply_transform)

        # Rotasi
        tk.Label(transform_inputs, text="Rotasi (°):", bg='#f0f8ff', 
                fg='#2d3748', font=('Segoe UI', 9)).grid(row=1, column=2, padx=5, sticky='w')
        self.rotation_var = tk.StringVar(value='0')
        self.rotation_entry = tk.Entry(transform_inputs, textvariable=self.rotation_var,
                                      width=10, state='disabled', font=('Segoe UI', 9))
        self.rotation_entry.grid(row=1, column=3, padx=5)
        self.rotation_entry.bind('<KeyRelease>', self.apply_transform)

        # Clear button
        clear_btn = tk.Button(self.root, text="Bersihkan Canvas", command=self.clear_canvas,
                             bg='#3182ce', fg='white', font=('Segoe UI', 12, 'bold'),
                             relief='raised', bd=3, pady=5)
        clear_btn.pack(fill='x', padx=10, pady=5)

        # Status bar
        self.status_var = tk.StringVar()
        status_bar = tk.Label(self.root, textvariable=self.status_var,
                             bg='#e6f3ff', fg='#2d3748', font=('Segoe UI', 10),
                             relief='sunken', bd=1, anchor='center')
        status_bar.pack(fill='x', side='bottom')

    def setup_bindings(self):
        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
        
        # Keyboard shortcuts
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-y>', lambda e: self.redo())
        self.root.bind('<Control-Z>', lambda e: self.redo())  # Shift+Ctrl+Z
        
        self.root.focus_set()

    def change_mode(self):
        self.current_mode = self.mode_var.get()
        self.selected_object = None
        self.update_transform_controls()
        self.redraw_canvas()
        
        if self.current_mode == 'select':
            self.canvas.configure(cursor='hand2')
            self.update_status('Mode pilih: Klik objek untuk memilih')
        else:
            self.canvas.configure(cursor='crosshair')
            self.update_status('Mode gambar: Pilih alat dan mulai menggambar')

    def change_tool(self):
        self.current_tool = self.tool_var.get()
        if self.current_mode == 'draw':
            tool_names = {'point': 'Titik', 'line': 'Garis', 
                         'rectangle': 'Persegi', 'ellipse': 'Ellipse'}
            self.update_status(f"Alat aktif: {tool_names[self.current_tool]}")

    def choose_color(self):
        color = colorchooser.askcolor(color=self.current_color)[1]
        if color:
            self.current_color = color

    def change_thickness(self, value):
        self.current_thickness = int(value)

    def on_mouse_down(self, event):
        if self.current_mode == 'select':
            self.select_object_at(event.x, event.y)
            return

        self.start_pos = (event.x, event.y)
        self.is_drawing = True

        if self.current_tool == 'point':
            self.draw_point(event.x, event.y)
            self.is_drawing = False

    def on_mouse_move(self, event):
        if not self.is_drawing or self.current_mode == 'select':
            return
        
        self.redraw_canvas()
        self.draw_preview(self.start_pos, (event.x, event.y))

    def on_mouse_up(self, event):
        if not self.is_drawing or self.current_mode == 'select':
            return
        
        self.is_drawing = False
        
        if self.current_tool != 'point':
            obj = DrawingObject(self.current_tool, self.start_pos, 
                              (event.x, event.y), self.current_color, 
                              self.current_thickness)
            self.objects.append(obj)
            self.save_state()
        
        self.redraw_canvas()
        tool_names = {'point': 'Titik', 'line': 'Garis', 
                     'rectangle': 'Persegi', 'ellipse': 'Ellipse'}
        self.update_status(f"{tool_names[self.current_tool]} berhasil digambar")

    def draw_point(self, x, y):
        obj = DrawingObject('point', (x, y), (x, y), 
                           self.current_color, self.current_thickness)
        self.objects.append(obj)
        self.save_state()
        self.redraw_canvas()

    def select_object_at(self, x, y):
        # Find the topmost object at the clicked position
        for obj in reversed(self.objects):
            if self.is_point_in_object((x, y), obj):
                self.selected_object = obj
                self.update_transform_controls()
                self.redraw_canvas()
                tool_names = {'point': 'Titik', 'line': 'Garis', 
                             'rectangle': 'Persegi', 'ellipse': 'Ellipse'}
                self.update_status(f"Objek {tool_names[obj.type]} dipilih")
                return
        
        # No object found
        self.selected_object = None
        self.update_transform_controls()
        self.redraw_canvas()
        self.update_status('Tidak ada objek yang dipilih')

    def is_point_in_object(self, point, obj):
        margin = 10
        x, y = point
        
        # Simple bounding box check
        min_x = min(obj.start[0], obj.end[0]) + obj.transform['translateX'] - margin
        max_x = max(obj.start[0], obj.end[0]) + obj.transform['translateX'] + margin
        min_y = min(obj.start[1], obj.end[1]) + obj.transform['translateY'] - margin
        max_y = max(obj.start[1], obj.end[1]) + obj.transform['translateY'] + margin
        
        return min_x <= x <= max_x and min_y <= y <= max_y

    def draw_preview(self, start, end):
        if self.current_tool == 'line':
            self.canvas.create_line(start[0], start[1], end[0], end[1],
                                   fill=self.current_color, width=self.current_thickness,
                                   capstyle='round', tags='preview')
        elif self.current_tool == 'rectangle':
            self.canvas.create_rectangle(start[0], start[1], end[0], end[1],
                                        outline=self.current_color, width=self.current_thickness,
                                        tags='preview')
        elif self.current_tool == 'ellipse':
            self.canvas.create_oval(start[0], start[1], end[0], end[1],
                                   outline=self.current_color, width=self.current_thickness,
                                   tags='preview')

    def draw_object(self, obj, is_selected=False):
        # Apply transformations
        start_x, start_y = obj.start
        end_x, end_y = obj.end
        
        # Apply translation
        start_x += obj.transform['translateX']
        start_y += obj.transform['translateY']
        end_x += obj.transform['translateX']
        end_y += obj.transform['translateY']
        
        # For scaling and rotation, we need to transform around the center
        center_x = (start_x + end_x) / 2
        center_y = (start_y + end_y) / 2
        
        # Apply scaling
        scale = obj.transform['scale']
        start_x = center_x + (start_x - center_x) * scale
        start_y = center_y + (start_y - center_y) * scale
        end_x = center_x + (end_x - center_x) * scale
        end_y = center_y + (end_y - center_y) * scale
        
        # Apply rotation
        rotation = math.radians(obj.transform['rotation'])
        if rotation != 0:
            # Rotate start point
            dx1, dy1 = start_x - center_x, start_y - center_y
            start_x = center_x + dx1 * math.cos(rotation) - dy1 * math.sin(rotation)
            start_y = center_y + dx1 * math.sin(rotation) + dy1 * math.cos(rotation)
            
            # Rotate end point
            dx2, dy2 = end_x - center_x, end_y - center_y
            end_x = center_x + dx2 * math.cos(rotation) - dy2 * math.sin(rotation)
            end_y = center_y + dx2 * math.sin(rotation) + dy2 * math.cos(rotation)

        color = obj.color
        thickness = obj.thickness
        
        if is_selected:
            color = '#ff6b6b'
            thickness = max(thickness, 2)

        if obj.type == 'point':
            radius = thickness
            self.canvas.create_oval(start_x - radius, start_y - radius,
                                   start_x + radius, start_y + radius,
                                   fill=obj.color, outline=color if is_selected else obj.color,
                                   width=2 if is_selected else 1)
            if is_selected:
                # Add dashed outline for selected point
                self.canvas.create_oval(start_x - radius - 3, start_y - radius - 3,
                                       start_x + radius + 3, start_y + radius + 3,
                                       outline=color, width=2, dash=(5, 5))
        elif obj.type == 'line':
            dash = (5, 5) if is_selected else ()
            self.canvas.create_line(start_x, start_y, end_x, end_y,
                                   fill=color, width=thickness, capstyle='round',
                                   dash=dash)
        elif obj.type == 'rectangle':
            dash = (5, 5) if is_selected else ()
            self.canvas.create_rectangle(start_x, start_y, end_x, end_y,
                                        outline=color, width=thickness, dash=dash)
        elif obj.type == 'ellipse':
            dash = (5, 5) if is_selected else ()
            self.canvas.create_oval(start_x, start_y, end_x, end_y,
                                   outline=color, width=thickness, dash=dash)

    def redraw_canvas(self):
        self.canvas.delete('all')
        for obj in self.objects:
            is_selected = self.selected_object and self.selected_object.id == obj.id
            self.draw_object(obj, is_selected)

    def apply_transform(self, event=None):
        if not self.selected_object:
            return

        try:
            self.selected_object.transform = {
                'translateX': float(self.translate_x_var.get() or 0),
                'translateY': float(self.translate_y_var.get() or 0),
                'scale': float(self.scale_var.get() or 1),
                'rotation': float(self.rotation_var.get() or 0)
            }
            self.redraw_canvas()
            # Save state after a short delay to avoid too many saves
            self.root.after(500, self.save_state)
        except ValueError:
            pass  # Ignore invalid input

    def update_transform_controls(self):
        entries = [self.translate_x_entry, self.translate_y_entry, 
                  self.scale_entry, self.rotation_entry]
        
        if self.selected_object:
            for entry in entries:
                entry.configure(state='normal')
            
            self.translate_x_var.set(str(self.selected_object.transform['translateX']))
            self.translate_y_var.set(str(self.selected_object.transform['translateY']))
            self.scale_var.set(str(self.selected_object.transform['scale']))
            self.rotation_var.set(str(self.selected_object.transform['rotation']))
        else:
            for entry in entries:
                entry.configure(state='disabled')
            
            self.translate_x_var.set('0')
            self.translate_y_var.set('0')
            self.scale_var.set('1.0')
            self.rotation_var.set('0')

    def save_state(self):
        # Remove any states after current step
        self.history = self.history[:self.history_step + 1]
        
        # Add new state (deep copy)
        state = []
        for obj in self.objects:
            obj_copy = DrawingObject(obj.type, obj.start, obj.end, obj.color, obj.thickness)
            obj_copy.transform = obj.transform.copy()
            obj_copy.id = obj.id
            state.append(obj_copy)
        
        self.history.append(state)
        self.history_step += 1
        
        # Limit history size
        if len(self.history) > 50:
            self.history.pop(0)
            self.history_step -= 1
        
        self.update_undo_redo_buttons()

    def undo(self):
        if self.history_step > 0:
            self.history_step -= 1
            self.objects = []
            for obj in self.history[self.history_step]:
                obj_copy = DrawingObject(obj.type, obj.start, obj.end, obj.color, obj.thickness)
                obj_copy.transform = obj.transform.copy()
                obj_copy.id = obj.id
                self.objects.append(obj_copy)
            
            self.selected_object = None
            self.update_transform_controls()
            self.redraw_canvas()
            self.update_undo_redo_buttons()
            self.update_status('Undo berhasil')

    def redo(self):
        if self.history_step < len(self.history) - 1:
            self.history_step += 1
            self.objects = []
            for obj in self.history[self.history_step]:
                obj_copy = DrawingObject(obj.type, obj.start, obj.end, obj.color, obj.thickness)
                obj_copy.transform = obj.transform.copy()
                obj_copy.id = obj.id
                self.objects.append(obj_copy)
            
            self.selected_object = None
            self.update_transform_controls()
            self.redraw_canvas()
            self.update_undo_redo_buttons()
            self.update_status('Redo berhasil')

    def update_undo_redo_buttons(self):
        self.undo_btn.configure(state='normal' if self.history_step > 0 else 'disabled')
        self.redo_btn.configure(state='normal' if self.history_step < len(self.history) - 1 else 'disabled')

    def clear_canvas(self):
        self.objects = []
        self.selected_object = None
        self.canvas.delete('all')
        self.update_transform_controls()
        self.save_state()
        self.update_status('Canvas dibersihkan')

    def update_status(self, message):
        self.status_var.set(message)

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()