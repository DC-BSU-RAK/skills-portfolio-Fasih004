# --- IMPORTS ---
import customtkinter as ctk            # Modern Tkinter library
from tkinter import messagebox         # Standard dialog boxes
from datetime import datetime

# --- CUSTOMTKINTER SETUP ---
ctk.set_appearance_mode("light")       # light theme
ctk.set_default_color_theme("blue")   # Primary color theme

class StudentManagerApp:
    """Main application class that builds UI and holds application state."""
    def __init__(self, root_window):
        # Root window setup
        self.root_window = root_window
        self.root_window.title("Student Manager")

        # Window configuration - maximise and set minimum size
        self.root_window.state('zoomed')
        self.root_window.minsize(1000, 700)

        # --- APPLICATION STATE ---
        # student_data holds records, which view is active and currently selected student
        self.student_data = {
            'records': {},             # dictionary keyed by student ID
            'active_view': 'dashboard',
            'current_student': None,
            'stats': {}
        }

        # Current logged in user display name and navi button state
        self.current_user_name = "Fasih"
        self.active_nav_btn = None

        # Load student data from file into application state
        self.load_student_data_from_file()

        # Build UI after loading data
        self.setup_user_interface()

    def load_student_data_from_file(self):
        file_path =  r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\Student Manager - Extension Problem\studentMarks.txt"
        try:
            with open(file_path, 'r') as data_file:
                lines_list = data_file.readlines()

                # If file unexpectedly empty, show error
                if len(lines_list) < 1:
                    messagebox.showerror("Error", "File is empty!")
                    return

                # First line is the count of students 
                total_students_count = int(lines_list[0].strip())
                for line_index in range(1, len(lines_list)):
                    line_data = lines_list[line_index].strip()
                    if line_data:
                        data_parts = line_data.split(',')
                        # Expect 6 comma-separated values per student
                        if len(data_parts) == 6:
                            student_id = data_parts[0].strip()
                            student_full_name = data_parts[1].strip()
                            coursework_mark_1 = int(data_parts[2].strip())
                            coursework_mark_2 = int(data_parts[3].strip())
                            coursework_mark_3 = int(data_parts[4].strip())
                            final_exam_mark = int(data_parts[5].strip())

                            # Store parsed values in the records dictionary
                            self.student_data['records'][student_id] = {
                                'name': student_full_name,
                                'student_number': student_id,
                                'coursework_1': coursework_mark_1,
                                'coursework_2': coursework_mark_2,
                                'coursework_3': coursework_mark_3,
                                'exam_mark': final_exam_mark
                            }
                print(f"Loaded {len(self.student_data['records'])} student records")

        except FileNotFoundError:
            # Show dialog and quit if file missing
            messagebox.showerror("Error", "studentMarks.txt file not found!")
            self.root_window.quit()
        except Exception as error_msg:
            messagebox.showerror("Error", f"Error loading data: {str(error_msg)}")
            self.root_window.quit()

    def calculate_student_statistics(self, student_record):
        """Calculate derived statistics for a single student record.
            total_coursework: sum of 3 coursework marks (out of 60)
            exam_mark: exam mark (out of 100)
            total_marks: sum of coursework + exam (out of 160)
            percentage: overall percentage (total / 160 * 100)
            grade: letter grade based on percentage thresholds
        """
        total_coursework = (student_record['coursework_1'] +
                           student_record['coursework_2'] +
                           student_record['coursework_3'])

        exam_mark_value = student_record['exam_mark']
        total_marks_sum = total_coursework + exam_mark_value
        overall_percentage = (total_marks_sum / 160) * 100

        # Grade thresholds
        if overall_percentage >= 70:
            grade_letter = 'A'
        elif overall_percentage >= 60:
            grade_letter = 'B'
        elif overall_percentage >= 50:
            grade_letter = 'C'
        elif overall_percentage >= 40:
            grade_letter = 'D'
        else:
            grade_letter = 'F'

        return {
            'total_coursework': total_coursework,
            'exam_mark': exam_mark_value,
            'total_marks': total_marks_sum,
            'percentage': overall_percentage,
            'grade': grade_letter
        }

    def setup_user_interface(self):
        """Setup the main window layout: left sidebar and main content area."""
        # Main container frame 
        main_container = ctk.CTkFrame(self.root_window, fg_color="#f0f4f8", corner_radius=0)
        main_container.pack(fill="both", expand=True, padx=30, pady=30)

        # Navigation sidebar and primary content area
        self.create_sidebar_navigation(main_container)
        self.create_main_content_area(main_container)

    def create_sidebar_navigation(self, parent):
        """left sidebar with navigation buttons and a logout button."""
        # Sidebar frame 
        sidebar_frame = ctk.CTkFrame(parent, fg_color="#6366f1", width=175, corner_radius=15)
        sidebar_frame.pack(side="left", fill="y", padx=(0, 10))
        sidebar_frame.pack_propagate(False)

        # Small logo button at top 
        logo_btn = ctk.CTkButton(
            sidebar_frame,
            text="📚",
            font=("Arial", 28, "bold"),
            fg_color="#4f46e5",
            hover_color="#4338ca",
            width=50,
            height=50,
            corner_radius=10
        )
        logo_btn.pack(pady=20, padx=15)

        # Navigation configuration: (label, handler function)
        nav_config = [
            ("⊞ Dashboard", self.show_dashboard_view),
            ("☰ All Students", self.show_all_students),
            ("👤 Student", self.show_individual_student),
            ("🏆 Top Score", self.show_highest_score_student),
            ("📉 Low Score", self.show_lowest_score_student),
            ("🔄 Sort Records", self.show_sort_records),
            ("➕ Add Student", self.show_add_student),
            ("🗑️ Delete Student", self.show_delete_student),
            ("✏️ Update Student", self.show_update_student),
        ]

        self.nav_buttons_list = []

        # Create a button per navigation item
        for text, command in nav_config:
            btn = ctk.CTkButton(
                sidebar_frame,
                text=text,
                font=("Arial", 13),
                fg_color="transparent",
                hover_color="#4f46e5",
                text_color="#e0e7ff",
                width=120,
                height=45,
                corner_radius=10,
                anchor="w",
                # A lambda wrapper is used to pass the button reference into navigate_to
                command=lambda cmd=command, b=None: self.navigate_to(cmd, b)
            )
            btn.configure(command=lambda cmd=command, b=btn: self.navigate_to(cmd, b))
            btn.pack(pady=8, padx=15)
            self.nav_buttons_list.append(btn)

        # Logout button fixed at bottom of sidebar
        logout_btn = ctk.CTkButton(
            sidebar_frame,
            text="Log Out",
            font=("Arial", 17),
            fg_color="transparent",
            hover_color="#ef4444",
            text_color="#e0e7ff",
            width=120,
            height=45,
            corner_radius=10,
            anchor="w",
            command=self.confirm_exit
        )
        logout_btn.pack(side="bottom", pady=20, padx=15)

    def navigate_to(self, command, button):
        """Handle navigation button active state and call view handlers.

        - Deactivates previously active nav button styling.
        - Activates clicked button styling.
        - Calls the view's handler function.
        """
        if self.active_nav_btn:
            # Reset previously active button colors
            self.active_nav_btn.configure(fg_color="transparent", text_color="#e0e7ff")

        # Set new active button and style it
        self.active_nav_btn = button
        button.configure(fg_color="#4f46e5", text_color="#FFFFFF")

        # Execute the associated view function
        if command:
            command()

    def create_main_content_area(self, parent):
        """Create the area to the right of the sidebar where pages are displayed."""
        content_container = ctk.CTkFrame(parent, fg_color="#ffffff", corner_radius=15)
        content_container.pack(side="left", fill="both", expand=True)

        # Header area with page title and user profile button
        header_frame = ctk.CTkFrame(content_container, fg_color="transparent", height=80)
        header_frame.pack(fill="x", padx=30, pady=(20, 0))
        header_frame.pack_propagate(False)

        # Title label for the current page
        self.page_title_label = ctk.CTkLabel(
            header_frame,
            text="Overview",
            font=("Arial", 28, "bold"),
            text_color="#1e293b"
        )
        self.page_title_label.pack(side="left", anchor="w")

        # Right-side header (profile button, etc.)
        right_header_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        right_header_frame.pack(side="right")

        profile_btn = ctk.CTkButton(
            right_header_frame,
            text=f"👤 {self.current_user_name}",
            font=("Arial", 12),
            fg_color="#6366f1",
            hover_color="#4f46e5",
            corner_radius=10,
            width=120,
            height=40
        )
        profile_btn.pack(side="left", padx=10)

        # Scrollable frame to hold page content (so long lists can scroll)
        self.content_display_frame = ctk.CTkScrollableFrame(
            content_container,
            fg_color="transparent",
            corner_radius=0
        )
        self.content_display_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Show default view (dashboard)
        self.show_dashboard_view()

        # Set the first navigation button as active visually if present
        if self.nav_buttons_list:
            self.active_nav_btn = self.nav_buttons_list[0]
            self.active_nav_btn.configure(fg_color="#4f46e5", text_color="#FFFFFF")

    def clear_content_display(self):
        """Remove all child widgets from the main content display area."""
        for widget in self.content_display_frame.winfo_children():
            widget.destroy()

    def show_dashboard_view(self):
        """Dashboard view:
        - Date and time display
        - Hero section with total students and class average
        - Circular stat cards for grade distribution
        - Recent students cards
        """
        self.clear_content_display()
        self.page_title_label.configure(text="📊 Dashboard")

        # Date and Time display at top
        datetime_frame = ctk.CTkFrame(self.content_display_frame, fg_color="transparent")
        datetime_frame.pack(fill="x", pady=(0, 15))
        
        current_date = datetime.now().strftime("%A, %d %B %Y")
        date_label = ctk.CTkLabel(
            datetime_frame,
            text=current_date,
            font=("Arial", 12),
            text_color="#64748b"
        )
        date_label.pack(side="left")
        
        self.time_label = ctk.CTkLabel(
            datetime_frame,
            text="",
            font=("Arial", 12),
            text_color="#64748b"
        )
        self.time_label.pack(side="right")
        
        def update_time():
            current_time = datetime.now().strftime("%I:%M:%S %p")
            self.time_label.configure(text=current_time)
            self.time_label.after(1000, update_time)
        
        update_time()

        # Hero section 
        hero_frame = ctk.CTkFrame(self.content_display_frame, fg_color="#6366f1", corner_radius=20, height=200)
        hero_frame.pack(fill="x", pady=(0, 30))
        hero_frame.pack_propagate(False)

        total_students = len(self.student_data['records'])

        # Compute average percentage across all students
        if total_students > 0:
            all_percentages = []
            for student_id, student_record in self.student_data['records'].items():
                stats = self.calculate_student_statistics(student_record)
                all_percentages.append(stats['percentage'])

            avg_percentage = sum(all_percentages) / len(all_percentages)
        else:
            avg_percentage = 0

        # Large total student count display
        ctk.CTkLabel(
            hero_frame,
            text=f"{total_students}",
            font=("Arial", 72, "bold"),
            text_color="#FFFFFF"
        ).place(relx=0.25, rely=0.35, anchor="center")

        ctk.CTkLabel(
            hero_frame,
            text="TOTAL STUDENTS",
            font=("Arial", 14),
            text_color="#e0e7ff"
        ).place(relx=0.25, rely=0.65, anchor="center")

        # Class average percentage display
        ctk.CTkLabel(
            hero_frame,
            text=f"{avg_percentage:.1f}%",
            font=("Arial", 72, "bold"),
            text_color="#FFFFFF"
        ).place(relx=0.75, rely=0.35, anchor="center")

        ctk.CTkLabel(
            hero_frame,
            text="CLASS AVERAGE",
            font=("Arial", 14),
            text_color="#e0e7ff"
        ).place(relx=0.75, rely=0.65, anchor="center")

        # Circular stat cards for grade distribution (A, B, C, D, F)
        circular_container = ctk.CTkFrame(self.content_display_frame, fg_color="transparent")
        circular_container.pack(fill="x", pady=(0, 30))

        if total_students > 0:
            # Count how many students in each grade
            grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
            for student_id, student_record in self.student_data['records'].items():
                stats = self.calculate_student_statistics(student_record)
                grade_counts[stats['grade']] += 1

            grade_colors = {
                'A': "#10b981",
                'B': "#3b82f6",
                'C': "#f59e0b",
                'D': "#f97316",
                'F': "#ef4444"
            }

            # Build a small circular card for each grade
            for idx, (grade, count) in enumerate(grade_counts.items()):
                card = ctk.CTkFrame(circular_container, fg_color="#f8fafc", corner_radius=100, width=140, height=140, border_width=2, border_color=grade_colors[grade])
                card.grid(row=0, column=idx, padx=15, pady=10)
                card.grid_propagate(False)

                ctk.CTkLabel(
                    card,
                    text=grade,
                    font=("Arial", 36, "bold"),
                    text_color=grade_colors[grade]
                ).place(relx=0.5, rely=0.35, anchor="center")

                ctk.CTkLabel(
                    card,
                    text=f"{count} students",
                    font=("Arial", 11),
                    text_color="#64748b"
                ).place(relx=0.5, rely=0.65, anchor="center")

        # Recent students list shown as cards (up to 6)
        ctk.CTkLabel(
            self.content_display_frame,
            text="📋 Recent Students",
            font=("Arial", 20, "bold"),
            text_color="#1e293b"
        ).pack(anchor="w", pady=(20, 15))

        cards_container = ctk.CTkFrame(self.content_display_frame, fg_color="transparent")
        cards_container.pack(fill="both", expand=True)

        # Show up to 6 recent student cards in a 3-column grid
        for idx, (student_id, student_record) in enumerate(list(self.student_data['records'].items())[:6]):
            stats = self.calculate_student_statistics(student_record)

            row = idx // 3
            col = idx % 3

            card = ctk.CTkFrame(cards_container, fg_color="#f8fafc", corner_radius=15, height=180, border_width=2, border_color="#e2e8f0")
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            cards_container.grid_columnconfigure(col, weight=1)
            card.grid_propagate(False)

            # Grade circle badge
            grade_bg = "#10b981" if stats['grade'] in ['A', 'B'] else "#f59e0b" if stats['grade'] == 'C' else "#ef4444"
            grade_circle = ctk.CTkFrame(card, fg_color=grade_bg, width=50, height=50, corner_radius=25)
            grade_circle.place(relx=0.5, rely=0.2, anchor="center")

            ctk.CTkLabel(
                grade_circle,
                text=stats['grade'],
                font=("Arial", 20, "bold"),
                text_color="#FFFFFF"
            ).place(relx=0.5, rely=0.5, anchor="center")

            # Student details on card
            ctk.CTkLabel(
                card,
                text=student_record['name'],
                font=("Arial", 14, "bold"),
                text_color="#1e293b"
            ).place(relx=0.5, rely=0.5, anchor="center")

            ctk.CTkLabel(
                card,
                text=f"{stats['percentage']:.1f}%",
                font=("Arial", 18, "bold"),
                text_color=grade_bg
            ).place(relx=0.5, rely=0.7, anchor="center")

            ctk.CTkLabel(
                card,
                text=f"ID: {student_record['student_number']}",
                font=("Arial", 9),
                text_color="#94a3b8"
            ).place(relx=0.5, rely=0.85, anchor="center")

    def show_all_students(self):
        """All Students view:
        - Groups students by grade into columns
        - Shows simple student cards with name, id and percentage
        """
        self.clear_content_display()
        self.page_title_label.configure(text="📚 All Students")

        if not self.student_data['records']:
            ctk.CTkLabel(
                self.content_display_frame,
                text="No student records found!",
                font=("Arial", 16),
                text_color="#64748b"
            ).pack(pady=50)
            return

        # Group students by their letter grade
        grade_groups = {'A': [], 'B': [], 'C': [], 'D': [], 'F': []}
        for student_id, student_record in self.student_data['records'].items():
            stats = self.calculate_student_statistics(student_record)
            grade_groups[stats['grade']].append((student_record, stats))

        # Container for columns
        columns_container = ctk.CTkFrame(self.content_display_frame, fg_color="transparent")
        columns_container.pack(fill="both", expand=True)

        grade_colors = {
            'A': "#10b981",
            'B': "#3b82f6",
            'C': "#f59e0b",
            'D': "#f97316",
            'F': "#ef4444"
        }

        grade_names = {
            'A': "Excellent",
            'B': "Good",
            'C': "Average",
            'D': "Below Average",
            'F': "Needs Help"
        }

        # Create a column for each grade
        for col_idx, (grade, students) in enumerate(grade_groups.items()):
            column = ctk.CTkFrame(columns_container, fg_color="#f8fafc", corner_radius=15, border_width=2, border_color="#e2e8f0")
            column.grid(row=0, column=col_idx, padx=8, pady=0, sticky="nsew")
            columns_container.grid_columnconfigure(col_idx, weight=1)

            # Column header shows grade and count
            header = ctk.CTkFrame(column, fg_color=grade_colors[grade], corner_radius=10, height=80)
            header.pack(fill="x", padx=10, pady=10)
            header.pack_propagate(False)

            ctk.CTkLabel(
                header,
                text=f"Grade {grade}",
                font=("Arial", 20, "bold"),
                text_color="#FFFFFF"
            ).place(relx=0.5, rely=0.35, anchor="center")

            ctk.CTkLabel(
                header,
                text=f"{grade_names[grade]} • {len(students)} students",
                font=("Arial", 10),
                text_color="#FFFFFF"
            ).place(relx=0.5, rely=0.65, anchor="center")

            # Student cards in the column
            for student_record, stats in students:
                student_card = ctk.CTkFrame(column, fg_color="#ffffff", corner_radius=10, height=120, border_width=1, border_color="#e2e8f0")
                student_card.pack(fill="x", padx=10, pady=8)
                student_card.pack_propagate(False)

                ctk.CTkLabel(
                    student_card,
                    text=student_record['name'],
                    font=("Arial", 13, "bold"),
                    text_color="#1e293b"
                ).pack(anchor="w", padx=15, pady=(15, 5))

                ctk.CTkLabel(
                    student_card,
                    text=f"ID: {student_record['student_number']}",
                    font=("Arial", 10),
                    text_color="#64748b"
                ).pack(anchor="w", padx=15, pady=2)

                ctk.CTkLabel(
                    student_card,
                    text=f"Score: {stats['percentage']:.1f}%",
                    font=("Arial", 12, "bold"),
                    text_color=grade_colors[grade]
                ).pack(anchor="w", padx=15, pady=(5, 10))

    def show_individual_student(self):
        """Individual Student view:
        - Dropdown to choose a student
        - Profile card with grade badge and breakdown of coursework and exam
        """
        self.clear_content_display()
        self.page_title_label.configure(text="👤 Student Profile")

        # Build list of student display strings for the dropdown: "Name (ID)"
        student_names_list = [f"{data['name']} ({sid})"
                             for sid, data in self.student_data['records'].items()]

        if not student_names_list:
            ctk.CTkLabel(
                self.content_display_frame,
                text="No student records found!",
                font=("Arial", 16),
                text_color="#888888"
            ).pack(pady=50)
            return

        # Selector row containing label and dropdown
        selector_frame = ctk.CTkFrame(self.content_display_frame, fg_color="#1a1a1a", corner_radius=15, height=100)
        selector_frame.pack(fill="x", pady=(0, 30))
        selector_frame.pack_propagate(False)

        ctk.CTkLabel(
            selector_frame,
            text="Select Student:",
            font=("Arial", 16, "bold"),
            text_color="#FFFFFF"
        ).place(relx=0.05, rely=0.5, anchor="w")

        # Dropdown to pick a student
        student_dropdown = ctk.CTkComboBox(
            selector_frame,
            values=student_names_list,
            font=("Arial", 14),
            width=500,
            height=50,
            corner_radius=10
        )
        student_dropdown.set(student_names_list[0])
        student_dropdown.place(relx=0.35, rely=0.5, anchor="w")

        # Frame where profile details will be shown
        result_frame = ctk.CTkFrame(self.content_display_frame, fg_color="transparent")
        result_frame.pack(fill="both", expand=True)

        def display_student():
            # Clear previous widgets inside the result area
            for widget in result_frame.winfo_children():
                widget.destroy()

            selected_text = student_dropdown.get()
            student_id = selected_text.split('(')[-1].strip(')')

            if student_id in self.student_data['records']:
                student_record = self.student_data['records'][student_id]
                stats = self.calculate_student_statistics(student_record)

                # Main profile card container
                profile_card = ctk.CTkFrame(result_frame, fg_color="#1a1a1a", corner_radius=20)
                profile_card.pack(fill="both", expand=True)

                # Left panel: avatar-like grade badge and basic info
                left_panel = ctk.CTkFrame(profile_card, fg_color="#242424", corner_radius=15, width=350)
                left_panel.pack(side="left", fill="y", padx=20, pady=20)
                left_panel.pack_propagate(False)

                # Large circular grade badge
                grade_bg = "#43a047" if stats['grade'] in ['A', 'B'] else "#fb8c00" if stats['grade'] == 'C' else "#e53935"
                grade_badge = ctk.CTkFrame(left_panel, fg_color=grade_bg, width=150, height=150, corner_radius=75)
                grade_badge.pack(pady=40)
                grade_badge.pack_propagate(False)

                ctk.CTkLabel(
                    grade_badge,
                    text=stats['grade'],
                    font=("Arial", 64, "bold"),
                    text_color="#FFFFFF"
                ).place(relx=0.5, rely=0.5, anchor="center")

                # Student name and ID
                ctk.CTkLabel(
                    left_panel,
                    text=student_record['name'],
                    font=("Arial", 22, "bold"),
                    text_color="#FFFFFF"
                ).pack(pady=(10, 5))

                ctk.CTkLabel(
                    left_panel,
                    text=f"Student ID: {student_record['student_number']}",
                    font=("Arial", 13),
                    text_color="#888888"
                ).pack(pady=(0, 30))

                # Overall score display
                ctk.CTkLabel(
                    left_panel,
                    text="Overall Score",
                    font=("Arial", 14),
                    text_color="#888888"
                ).pack()

                ctk.CTkLabel(
                    left_panel,
                    text=f"{stats['percentage']:.2f}%",
                    font=("Arial", 48, "bold"),
                    text_color=grade_bg
                ).pack(pady=10)

                # Right panel: detailed breakdown and progress bars
                right_panel = ctk.CTkFrame(profile_card, fg_color="transparent")
                right_panel.pack(side="left", fill="both", expand=True, padx=20, pady=20)

                ctk.CTkLabel(
                    right_panel,
                    text="Performance Breakdown",
                    font=("Arial", 20, "bold"),
                    text_color="#FFFFFF"
                ).pack(anchor="w", pady=(0, 20))

                # Small circular-like cards for each coursework
                circles_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
                circles_frame.pack(fill="x", pady=20)

                coursework_data = [
                    ("Coursework 1", student_record['coursework_1'], 20, "#1e88e5"),
                    ("Coursework 2", student_record['coursework_2'], 20, "#43a047"),
                    ("Coursework 3", student_record['coursework_3'], 20, "#fb8c00"),
                ]

                for idx, (label, score, max_score, color) in enumerate(coursework_data):
                    circle_card = ctk.CTkFrame(circles_frame, fg_color="#242424", corner_radius=15, width=180, height=180)
                    circle_card.grid(row=0, column=idx, padx=15, pady=10)
                    circle_card.grid_propagate(False)

                    percentage = (score / max_score) * 100

                    # Show numeric score and label
                    ctk.CTkLabel(
                        circle_card,
                        text=f"{score}/{max_score}",
                        font=("Arial", 28, "bold"),
                        text_color=color
                    ).place(relx=0.5, rely=0.4, anchor="center")

                    ctk.CTkLabel(
                        circle_card,
                        text=label,
                        font=("Arial", 11),
                        text_color="#AAAAAA"
                    ).place(relx=0.5, rely=0.65, anchor="center")

                # Final exam section with larger progress bar
                exam_frame = ctk.CTkFrame(right_panel, fg_color="#242424", corner_radius=15, height=150)
                exam_frame.pack(fill="x", pady=20)
                exam_frame.pack_propagate(False)

                ctk.CTkLabel(
                    exam_frame,
                    text="Final Examination",
                    font=("Arial", 16, "bold"),
                    text_color="#FFFFFF"
                ).place(relx=0.05, rely=0.3, anchor="w")

                ctk.CTkLabel(
                    exam_frame,
                    text=f"{stats['exam_mark']}/100",
                    font=("Arial", 42, "bold"),
                    text_color="#8e24aa"
                ).place(relx=0.05, rely=0.7, anchor="w")

                # Progress bar widget that shows exam percentage filled
                exam_percentage = (stats['exam_mark'] / 100) * 100
                ctk.CTkProgressBar(
                    exam_frame,
                    width=600,
                    height=15,
                    progress_color="#8e24aa"
                ).place(relx=0.95, rely=0.5, anchor="e")
                exam_frame.winfo_children()[-1].set(exam_percentage / 100)

        # View Profile button triggers display_student callback
        view_btn = ctk.CTkButton(
            selector_frame,
            text="View Profile →",
            font=("Arial", 14, "bold"),
            fg_color="#1e88e5",
            hover_color="#1565c0",
            corner_radius=10,
            width=150,
            height=50,
            command=display_student
        )
        view_btn.place(relx=0.95, rely=0.5, anchor="e")

        # Show first student's profile by default
        display_student()

    def show_highest_score_student(self):
        """Top Performer view:
        - Shows only the top student with full details
        """
        self.clear_content_display()
        self.page_title_label.configure(text="🏆 Top Performer")

        if not self.student_data['records']:
            ctk.CTkLabel(
                self.content_display_frame,
                text="No student records found!",
                font=("Arial", 16),
                text_color="#888888"
            ).pack(pady=50)
            return

        # Find the top student
        highest_percentage = -1
        top_student_record = None
        top_student_stats = None

        for student_id, student_record in self.student_data['records'].items():
            stats = self.calculate_student_statistics(student_record)
            if stats['percentage'] > highest_percentage:
                highest_percentage = stats['percentage']
                top_student_record = student_record
                top_student_stats = stats

        if not top_student_record or not top_student_stats:
            ctk.CTkLabel(
                self.content_display_frame,
                text="No student data available!",
                font=("Arial", 16),
                text_color="#888888"
            ).pack(pady=50)
            return

        # Top achievement banner
        banner = ctk.CTkFrame(self.content_display_frame, fg_color="#8B4513", corner_radius=20)
        banner.pack(fill="x", padx=10, pady=(0, 20))
        
        banner_content = ctk.CTkFrame(banner, fg_color="#D4AF37", corner_radius=15)
        banner_content.pack(fill="both", expand=True, padx=8, pady=8)
        
        ctk.CTkLabel(
            banner_content,
            text="═══════════════════════════════════════",
            font=("Courier", 12, "bold"),
            text_color="#5E4A3C"
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            banner_content,
            text="⭐ TOP ACADEMIC PERFORMER ⭐",
            font=("Arial", 24, "bold"),
            text_color="#8B4513"
        ).pack(pady=5)
        
        ctk.CTkLabel(
            banner_content,
            text="═══════════════════════════════════════",
            font=("Courier", 12, "bold"),
            text_color="#5E4A3C"
        ).pack(pady=(5, 15))
        
        # Main podium card
        podium_container = ctk.CTkFrame(self.content_display_frame, fg_color="transparent")
        podium_container.pack(fill="both", expand=True, padx=10)
        
        podium = ctk.CTkFrame(podium_container, fg_color="#1a1a1a", corner_radius=20)
        podium.pack(fill="both", expand=True)
        
        # Gold stripe at top
        stripe_container = ctk.CTkFrame(podium, fg_color="#AA6005", height=25, corner_radius=0)
        stripe_container.pack(fill="x")
        stripe_container.pack_propagate(False)
        
        colors = ["#FFD700", "#C0C0C0", "#FFD700", "#C0C0C0", "#FFD700"]
        for i, color in enumerate(colors):
            ctk.CTkFrame(stripe_container, fg_color=color, width=200).pack(side="left", fill="y", expand=True)
        
        podium_content = ctk.CTkFrame(podium, fg_color="#1a1a1a")
        podium_content.pack(fill="both", expand=True, padx=60, pady=30)
        
        # Medal section
        medal_section = ctk.CTkFrame(podium_content, fg_color="transparent")
        medal_section.pack(pady=(10, 15))
        
        medals_frame = ctk.CTkFrame(medal_section, fg_color="transparent")
        medals_frame.pack()
        
        ctk.CTkLabel(
            medals_frame,
            text="🥈",
            font=("Arial", 28),
            text_color="#AAAAAA"
        ).pack(side="left", padx=8)
        
        center_medal = ctk.CTkFrame(medals_frame, fg_color="#FFD700", corner_radius=50, width=100, height=100)
        center_medal.pack(side="left", padx=15)
        center_medal.pack_propagate(False)
        
        ctk.CTkLabel(
            center_medal,
            text="🥇",
            font=("Arial", 50)
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(
            medals_frame,
            text="🥉",
            font=("Arial", 28),
            text_color="#AAAAAA"
        ).pack(side="left", padx=8)
        
        # Rank badge
        rank_badge = ctk.CTkFrame(podium_content, fg_color="#8B4513", corner_radius=10)
        rank_badge.pack(pady=10)
        
        ctk.CTkLabel(
            rank_badge,
            text="RANK #1",
            font=("Arial", 16, "bold"),
            text_color="#FFD700"
        ).pack(padx=30, pady=8)
        
        # Student name section
        name_section = ctk.CTkFrame(podium_content, fg_color="transparent")
        name_section.pack(pady=15)
        
        ctk.CTkLabel(
            name_section,
            text="━━━━━━━━━━",
            font=("Arial", 14),
            text_color="#D4AF37"
        ).pack()
        
        ctk.CTkLabel(
            name_section,
            text=top_student_record['name'],
            font=("Georgia", 28, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=8)
        
        ctk.CTkLabel(
            name_section,
            text="━━━━━━━━━━",
            font=("Arial", 14),
            text_color="#D4AF37"
        ).pack()
        
        # ID ribbon
        ribbon = ctk.CTkFrame(podium_content, fg_color="#5E4A3C", corner_radius=10)
        ribbon.pack(pady=10)
        
        ctk.CTkLabel(
            ribbon,
            text=f"ID: {top_student_record['student_number']}",
            font=("Arial", 14, "bold"),
            text_color="white"
        ).pack(padx=35, pady=8)
        
        # Score showcase
        scores_grid = ctk.CTkFrame(podium_content, fg_color="transparent")
        scores_grid.pack(pady=20, fill="x", padx=20)
        
        score_col = ctk.CTkFrame(scores_grid, fg_color="transparent")
        score_col.pack(fill="both", expand=True, padx=10)
        
        perc_box = ctk.CTkFrame(score_col, fg_color="#E8F5E9", corner_radius=15)
        perc_box.pack(fill="both", expand=True, ipady=20)
        
        ctk.CTkLabel(
            perc_box,
            text="OVERALL SCORE",
            font=("Arial", 14, "bold"),
            text_color="#2E7D32"
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            perc_box,
            text=f"{top_student_stats['percentage']:.2f}%",
            font=("Arial", 48, "bold"),
            text_color="#4CAF50"
        ).pack(pady=5)
        
        ctk.CTkLabel(
            perc_box,
            text=f"Grade: {top_student_stats['grade']}",
            font=("Arial", 18, "bold"),
            text_color="#2E7D32"
        ).pack(pady=(5, 15))
        
        # Details section
        details_frame = ctk.CTkFrame(self.content_display_frame, fg_color="#242424", corner_radius=20)
        details_frame.pack(fill="x", pady=20, padx=10)
        
        ctk.CTkLabel(
            details_frame,
            text="🏆 Champion Details",
            font=("Arial", 20, "bold"),
            text_color="#FFD700"
        ).pack(pady=15)
        
        info_grid = ctk.CTkFrame(details_frame, fg_color="transparent")
        info_grid.pack(fill="x", padx=30, pady=(0, 20))
        
        details = [
            ("Coursework Total", f"{top_student_stats['total_coursework']}/60"),
            ("Exam Mark", f"{top_student_stats['exam_mark']}/100"),
            ("Total Marks", f"{top_student_stats['total_marks']}/160"),
        ]
        
        for idx, (label, value) in enumerate(details):
            col = idx % 3
            
            detail_card = ctk.CTkFrame(info_grid, fg_color="#1a1a1a", corner_radius=10, height=90)
            detail_card.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
            info_grid.grid_columnconfigure(col, weight=1)
            detail_card.grid_propagate(False)
            
            ctk.CTkLabel(
                detail_card,
                text=label,
                font=("Arial", 12),
                text_color="#888888"
            ).pack(pady=(20, 5))
            
            ctk.CTkLabel(
                detail_card,
                text=value,
                font=("Arial", 22, "bold"),
                text_color="#FFD700"
            ).pack()

    def show_lowest_score_student(self):
        """Student Support view:
        - Finds the lowest-performing student and shows action plan and contact CTA.
        """
        self.clear_content_display()
        self.page_title_label.configure(text="📉 Needs Improvement")

        if not self.student_data['records']:
            ctk.CTkLabel(
                self.content_display_frame,
                text="No student records found!",
                font=("Arial", 16),
                text_color="#888888"
            ).pack(pady=50)
            return

        # Find lowest percentage and corresponding student ID
        lowest_percentage = 101
        bottom_student_id = None

        for student_id, student_record in self.student_data['records'].items():
            stats = self.calculate_student_statistics(student_record)
            if stats['percentage'] < lowest_percentage:
                lowest_percentage = stats['percentage']
                bottom_student_id = student_id

        if bottom_student_id:
            student_record = self.student_data['records'][bottom_student_id]
            stats = self.calculate_student_statistics(student_record)

            # Attention banner at the top - softer design
            alert_banner = ctk.CTkFrame(self.content_display_frame, fg_color="#ff9800", corner_radius=15, height=100)
            alert_banner.pack(fill="x", pady=(0, 25))
            alert_banner.pack_propagate(False)

            ctk.CTkLabel(
                alert_banner,
                text="💡 STUDENT REQUIRING SUPPORT",
                font=("Arial", 24, "bold"),
                text_color="#FFFFFF"
            ).place(relx=0.5, rely=0.4, anchor="center")

            ctk.CTkLabel(
                alert_banner,
                text="Let's help this student improve their academic performance",
                font=("Arial", 13),
                text_color="#FFFFFF"
            ).place(relx=0.5, rely=0.7, anchor="center")

            # Main support card with student info, scores and action plan
            support_card = ctk.CTkFrame(self.content_display_frame, fg_color="#1a1a1a", corner_radius=20)
            support_card.pack(fill="both", expand=True)

            # Info section: left = details, right = big score box
            info_section = ctk.CTkFrame(support_card, fg_color="#242424", corner_radius=15)
            info_section.pack(fill="x", padx=20, pady=20)

            # Left detailed information
            left_info = ctk.CTkFrame(info_section, fg_color="transparent")
            left_info.pack(side="left", fill="both", expand=True, padx=20, pady=20)

            ctk.CTkLabel(
                left_info,
                text=student_record['name'],
                font=("Arial", 26, "bold"),
                text_color="#FFFFFF"
            ).pack(anchor="w", pady=(0, 5))

            ctk.CTkLabel(
                left_info,
                text=f"Student ID: {student_record['student_number']}",
                font=("Arial", 14),
                text_color="#888888"
            ).pack(anchor="w", pady=(0, 20))

            ctk.CTkLabel(
                left_info,
                text=f"Current Grade: {stats['grade']}",
                font=("Arial", 16, "bold"),
                text_color="#ff9800"
            ).pack(anchor="w")

            # Right big score display 
            right_info = ctk.CTkFrame(info_section, fg_color="#fb8c00", corner_radius=15, width=200, height=200)
            right_info.pack(side="right", padx=20, pady=20)
            right_info.pack_propagate(False)

            ctk.CTkLabel(
                right_info,
                text="Overall Score",
                font=("Arial", 14),
                text_color="#FFFFFF"
            ).place(relx=0.5, rely=0.3, anchor="center")

            ctk.CTkLabel(
                right_info,
                text=f"{stats['percentage']:.2f}%",
                font=("Arial", 36, "bold"),
                text_color="#FFFFFF"
            ).place(relx=0.5, rely=0.7, anchor="center")

            # Performance breakdown section with progress bars for each score item
            breakdown_frame = ctk.CTkFrame(support_card, fg_color="transparent")
            breakdown_frame.pack(fill="x", padx=20, pady=20)

            ctk.CTkLabel(
                breakdown_frame,
                text="📊 Performance Overview",
                font=("Arial", 20, "bold"),
                text_color="#FFFFFF"
            ).pack(anchor="w", pady=(0, 15))

            scores_data = [
                ("Coursework 1", student_record['coursework_1'], 20, "#1e88e5"),
                ("Coursework 2", student_record['coursework_2'], 20, "#43a047"),
                ("Coursework 3", student_record['coursework_3'], 20, "#fb8c00"),
                ("Final Exam", stats['exam_mark'], 100, "#8e24aa"),
            ]

            for label, score, max_score, color in scores_data:
                # Each score is a horizontal bar with label and percentage
                score_frame = ctk.CTkFrame(breakdown_frame, fg_color="#242424", corner_radius=10, height=70)
                score_frame.pack(fill="x", pady=8)
                score_frame.pack_propagate(False)

                ctk.CTkLabel(
                    score_frame,
                    text=label,
                    font=("Arial", 14, "bold"),
                    text_color="#FFFFFF"
                ).place(relx=0.05, rely=0.3, anchor="w")

                ctk.CTkLabel(
                    score_frame,
                    text=f"{score}/{max_score}",
                    font=("Arial", 18, "bold"),
                    text_color=color
                ).place(relx=0.05, rely=0.7, anchor="w")

                # Progress bar visualising the fraction achieved
                percentage = score / max_score
                bar = ctk.CTkProgressBar(
                    score_frame,
                    width=400,
                    height=20,
                    progress_color=color,
                    fg_color="#1a1a1a"
                )
                bar.place(relx=0.95, rely=0.5, anchor="e")
                bar.set(percentage)

                # Numeric percent text near the bar
                ctk.CTkLabel(
                    score_frame,
                    text=f"{percentage*100:.0f}%",
                    font=("Arial", 12, "bold"),
                    text_color="#AAAAAA"
                ).place(relx=0.85, rely=0.5, anchor="e")

            # Recommended action plan section with suggested interventions
            action_frame = ctk.CTkFrame(support_card, fg_color="#2d4a3d", corner_radius=15)
            action_frame.pack(fill="x", padx=20, pady=20)

            ctk.CTkLabel(
                action_frame,
                text="✨ Improvement Action Plan",
                font=("Arial", 18, "bold"),
                text_color="#FFFFFF"
            ).pack(anchor="w", padx=20, pady=(20, 10))

            actions = [
                "Arrange personalized tutoring sessions to address knowledge gaps",
                "Identify and focus on weak subject areas through targeted practice",
                "Develop a customized study schedule with achievable milestones",
                "Implement weekly progress monitoring and feedback sessions",
                "Encourage participation in peer study groups for collaborative learning"
            ]

            # List of recommended actions
            for action in actions:
                action_item = ctk.CTkFrame(action_frame, fg_color="#3d5a3d", corner_radius=8)
                action_item.pack(fill="x", padx=20, pady=5)

                ctk.CTkLabel(
                    action_item,
                    text=f"• {action}",
                    font=("Arial", 13),
                    text_color="#FFFFFF"
                ).pack(anchor="w", padx=15, pady=12)

            # Contact button placeholder 
            ctk.CTkButton(
                action_frame,
                text="📧 Reach Out to Student",
                font=("Arial", 14, "bold"),
                fg_color="#fb8c00",
                hover_color="#f57c00",
                corner_radius=10,
                width=200,
                height=45
            ).pack(pady=20)

    def confirm_exit(self):
        """Ask the user to confirm quitting the application."""
        result = messagebox.askyesno("Quit", "Are you sure you want to quit?")
        if result:
            self.root_window.quit()

    def save_to_file(self):
        """Save all student records back to the file"""
        file_path = r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\Student Manager - Extension Problem\studentMarks.txt"
        
        try:
            with open(file_path, 'w') as file:
                # Write total number of students
                file.write(f"{len(self.student_data['records'])}\n")
                
                # Write each student record
                for student_id, record in self.student_data['records'].items():
                    line = f"{record['student_number']},{record['name']},{record['coursework_1']},{record['coursework_2']},{record['coursework_3']},{record['exam_mark']}\n"
                    file.write(line)
            
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
            return False

    def show_sort_records(self):
        """Sort student records view"""
        self.clear_content_display()
        self.page_title_label.configure(text="🔄 Sort Student Records")
        
        if not self.student_data['records']:
            ctk.CTkLabel(
                self.content_display_frame,
                text="No student records found!",
                font=("Arial", 16),
                text_color="#64748b"
            ).pack(pady=50)
            return
        
        # Sort options frame
        options_frame = ctk.CTkFrame(self.content_display_frame, fg_color="#f8fafc", corner_radius=15, border_width=2, border_color="#e2e8f0")
        options_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            options_frame,
            text="Sort Options",
            font=("Arial", 20, "bold"),
            text_color="#1e293b"
        ).pack(pady=15)
        
        # Sort criteria
        criteria_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        criteria_frame.pack(pady=10)
        
        ctk.CTkLabel(
            criteria_frame,
            text="Sort By:",
            font=("Arial", 14, "bold"),
            text_color="#1e293b"
        ).pack(side="left", padx=(20, 10))
        
        sort_var = ctk.StringVar(value="percentage")
        
        ctk.CTkRadioButton(
            criteria_frame,
            text="Percentage",
            variable=sort_var,
            value="percentage",
            font=("Arial", 12),
            text_color="#1e293b",
            fg_color="#6366f1"
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            criteria_frame,
            text="Name",
            variable=sort_var,
            value="name",
            font=("Arial", 12),
            text_color="#1e293b",
            fg_color="#6366f1"
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            criteria_frame,
            text="Student ID",
            variable=sort_var,
            value="id",
            font=("Arial", 12),
            text_color="#1e293b",
            fg_color="#6366f1"
        ).pack(side="left", padx=10)
        
        # Order frame
        order_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        order_frame.pack(pady=10)
        
        ctk.CTkLabel(
            order_frame,
            text="Order:",
            font=("Arial", 14, "bold"),
            text_color="#1e293b"
        ).pack(side="left", padx=(20, 10))
        
        order_var = ctk.StringVar(value="desc")
        
        ctk.CTkRadioButton(
            order_frame,
            text="Ascending",
            variable=order_var,
            value="asc",
            font=("Arial", 12),
            text_color="#1e293b",
            fg_color="#6366f1"
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            order_frame,
            text="Descending",
            variable=order_var,
            value="desc",
            font=("Arial", 12),
            text_color="#1e293b",
            fg_color="#6366f1"
        ).pack(side="left", padx=10)
        
        # Results frame
        results_frame = ctk.CTkScrollableFrame(self.content_display_frame,height=500, fg_color="transparent")
        results_frame.pack(fill="both", expand=True)
        
        def perform_sort():
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            # Get all students with stats
            students_list = []
            for student_id, record in self.student_data['records'].items():
                stats = self.calculate_student_statistics(record)
                students_list.append((record, stats))
            
            # Sort based on criteria
            if sort_var.get() == "percentage":
                students_list.sort(key=lambda x: x[1]['percentage'], reverse=(order_var.get() == "desc"))
            elif sort_var.get() == "name":
                students_list.sort(key=lambda x: x[0]['name'], reverse=(order_var.get() == "desc"))
            else:  # id
                students_list.sort(key=lambda x: x[0]['student_number'], reverse=(order_var.get() == "desc"))
            
            # Display sorted results
            grade_colors = {
                'A': "#10b981",
                'B': "#3b82f6",
                'C': "#f59e0b",
                'D': "#f97316",
                'F': "#ef4444"
            }
            
            for idx, (record, stats) in enumerate(students_list):
                card = ctk.CTkFrame(results_frame, fg_color="#f8fafc", corner_radius=10, height=100, border_width=2, border_color="#e2e8f0")
                card.pack(fill="x", pady=5)
                card.pack_propagate(False)
                
                # Rank badge
                rank_badge = ctk.CTkFrame(card, fg_color="#6366f1", corner_radius=8, width=50, height=50)
                rank_badge.place(relx=0.02, rely=0.5, anchor="w")
                rank_badge.pack_propagate(False)
                
                ctk.CTkLabel(
                    rank_badge,
                    text=f"#{idx+1}",
                    font=("Arial", 14, "bold"),
                    text_color="#ffffff"
                ).place(relx=0.5, rely=0.5, anchor="center")
                
                # Student info
                info_frame = ctk.CTkFrame(card, fg_color="transparent")
                info_frame.place(relx=0.12, rely=0.3, anchor="w")
                
                ctk.CTkLabel(
                    info_frame,
                    text=record['name'],
                    font=("Arial", 14, "bold"),
                    text_color="#1e293b"
                ).pack(anchor="w")
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"ID: {record['student_number']}",
                    font=("Arial", 11),
                    text_color="#64748b"
                ).pack(anchor="w")
                
                # Stats on right
                stats_frame = ctk.CTkFrame(card, fg_color="transparent")
                stats_frame.place(relx=0.98, rely=0.5, anchor="e")
                
                ctk.CTkLabel(
                    stats_frame,
                    text=f"{stats['percentage']:.1f}%",
                    font=("Arial", 20, "bold"),
                    text_color=grade_colors[stats['grade']]
                ).pack(side="left", padx=10)
                
                grade_badge = ctk.CTkFrame(stats_frame, fg_color=grade_colors[stats['grade']], corner_radius=8, width=40, height=40)
                grade_badge.pack(side="left", padx=(0, 10))
                grade_badge.pack_propagate(False)
                
                ctk.CTkLabel(
                    grade_badge,
                    text=stats['grade'],
                    font=("Arial", 16, "bold"),
                    text_color="#ffffff"
                ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Sort button
        ctk.CTkButton(
            options_frame,
            text="🔄 Apply Sort",
            font=("Arial", 14, "bold"),
            fg_color="#6366f1",
            hover_color="#4f46e5",
            corner_radius=10,
            width=150,
            height=40,
            command=perform_sort
        ).pack(pady=15)
        
        # Initial sort
        perform_sort()

    def show_add_student(self):
        """Add new student view"""
        self.clear_content_display()
        self.page_title_label.configure(text="➕ Add New Student")
        
        # Form frame
        form_frame = ctk.CTkFrame(self.content_display_frame, fg_color="#f8fafc", corner_radius=15, border_width=2, border_color="#e2e8f0")
        form_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        ctk.CTkLabel(
            form_frame,
            text="Student Information Form",
            font=("Arial", 22, "bold"),
            text_color="#1e293b"
        ).pack(pady=20)
        
        # Entry fields
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(pady=20, padx=40, fill="x")
        
        entries = {}
        fields = [
            ("Student ID", "student_id"),
            ("Full Name", "name"),
            ("Coursework 1 (out of 20)", "cw1"),
            ("Coursework 2 (out of 20)", "cw2"),
            ("Coursework 3 (out of 20)", "cw3"),
            ("Exam Mark (out of 100)", "exam")
        ]
        
        for label, key in fields:
            field_container = ctk.CTkFrame(fields_frame, fg_color="transparent")
            field_container.pack(fill="x", pady=10)
            
            ctk.CTkLabel(
                field_container,
                text=label,
                font=("Arial", 13, "bold"),
                text_color="#1e293b",
                width=200,
                anchor="w"
            ).pack(side="left")
            
            entry = ctk.CTkEntry(
                field_container,
                font=("Arial", 13),
                width=300,
                height=40,
                corner_radius=8,
                border_width=2,
                border_color="#e2e8f0"
            )
            entry.pack(side="left", padx=20)
            entries[key] = entry
        
        # Status label
        status_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=("Arial", 12),
            text_color="#ef4444"
        )
        status_label.pack(pady=10)
        
        def add_student():
            # Validate inputs
            student_id = entries['student_id'].get().strip()
            name = entries['name'].get().strip()
            
            if not student_id or not name:
                status_label.configure(text="❌ Please fill in all fields", text_color="#ef4444")
                return
            
            if student_id in self.student_data['records']:
                status_label.configure(text="❌ Student ID already exists!", text_color="#ef4444")
                return
            
            try:
                cw1 = int(entries['cw1'].get().strip())
                cw2 = int(entries['cw2'].get().strip())
                cw3 = int(entries['cw3'].get().strip())
                exam = int(entries['exam'].get().strip())
                
                if not (0 <= cw1 <= 20 and 0 <= cw2 <= 20 and 0 <= cw3 <= 20):
                    status_label.configure(text="❌ Coursework marks must be between 0-20", text_color="#ef4444")
                    return
                
                if not (0 <= exam <= 100):
                    status_label.configure(text="❌ Exam mark must be between 0-100", text_color="#ef4444")
                    return
                
            except ValueError:
                status_label.configure(text="❌ Please enter valid numbers for marks", text_color="#ef4444")
                return
            
            # Add to records
            self.student_data['records'][student_id] = {
                'name': name,
                'student_number': student_id,
                'coursework_1': cw1,
                'coursework_2': cw2,
                'coursework_3': cw3,
                'exam_mark': exam
            }
            
            # Save to file
            if self.save_to_file():
                status_label.configure(text="✅ Student added successfully!", text_color="#10b981")
                
                # Clear entries
                for entry in entries.values():
                    entry.delete(0, 'end')
                
                # Show success message
                messagebox.showinfo("Success", f"Student {name} has been added successfully!")
            else:
                status_label.configure(text="❌ Failed to save to file", text_color="#ef4444")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        ctk.CTkButton(
            buttons_frame,
            text="➕ Add Student",
            font=("Arial", 14, "bold"),
            fg_color="#10b981",
            hover_color="#059669",
            corner_radius=10,
            width=150,
            height=45,
            command=add_student
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="🔄 Clear Form",
            font=("Arial", 14, "bold"),
            fg_color="#64748b",
            hover_color="#475569",
            corner_radius=10,
            width=150,
            height=45,
            command=lambda: [entry.delete(0, 'end') for entry in entries.values()]
        ).pack(side="left", padx=10)

    def show_delete_student(self):
        """Delete student view"""
        self.clear_content_display()
        self.page_title_label.configure(text="🗑️ Delete Student Record")
        
        if not self.student_data['records']:
            ctk.CTkLabel(
                self.content_display_frame,
                text="No student records found!",
                font=("Arial", 16),
                text_color="#64748b"
            ).pack(pady=50)
            return
        
        # Search frame
        search_frame = ctk.CTkFrame(self.content_display_frame, fg_color="#f8fafc", corner_radius=15, border_width=2, border_color="#e2e8f0", height=120)
        search_frame.pack(fill="x", pady=(0, 20))
        search_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            search_frame,
            text="Search Student to Delete",
            font=("Arial", 18, "bold"),
            text_color="#1e293b"
        ).pack(pady=15)
        
        search_container = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_container.pack()
        
        search_entry = ctk.CTkEntry(
            search_container,
            placeholder_text="Enter Student ID or Name",
            font=("Arial", 13),
            width=400,
            height=40,
            corner_radius=8,
            border_width=2,
            border_color="#e2e8f0"
        )
        search_entry.pack(side="left", padx=10)
        
        # Results frame
        results_frame = ctk.CTkScrollableFrame(self.content_display_frame, height=500 ,fg_color="transparent")
        results_frame.pack(fill="both", expand=True)
        
        def search_students():
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            search_term = search_entry.get().strip().lower()
            
            if not search_term:
                # Show all students
                matching_students = list(self.student_data['records'].items())
            else:
                matching_students = [
                    (sid, record) for sid, record in self.student_data['records'].items()
                    if search_term in sid.lower() or search_term in record['name'].lower()
                ]
            
            if not matching_students:
                ctk.CTkLabel(
                    results_frame,
                    text="No matching students found",
                    font=("Arial", 14),
                    text_color="#64748b"
                ).pack(pady=30)
                return
            
            for student_id, record in matching_students:
                stats = self.calculate_student_statistics(record)
                
                card = ctk.CTkFrame(results_frame, fg_color="#f8fafc", corner_radius=10, height=100, border_width=2, border_color="#e2e8f0")
                card.pack(fill="x", pady=5)
                card.pack_propagate(False)
                
                # Student info
                info_frame = ctk.CTkFrame(card, fg_color="transparent")
                info_frame.place(relx=0.02, rely=0.5, anchor="w")
                
                ctk.CTkLabel(
                    info_frame,
                    text=record['name'],
                    font=("Arial", 14, "bold"),
                    text_color="#1e293b"
                ).pack(anchor="w", padx=10)
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"ID: {record['student_number']} | Score: {stats['percentage']:.1f}% | Grade: {stats['grade']}",
                    font=("Arial", 11),
                    text_color="#64748b"
                ).pack(anchor="w", padx=10)
                
                # Delete button
                def delete_student(sid=student_id, sname=record['name']):
                    result = messagebox.askyesno(
                        "Confirm Delete",
                        f"Are you sure you want to delete {sname}?\n\nThis action cannot be undone!"
                    )
                    
                    if result:
                        del self.student_data['records'][sid]
                        if self.save_to_file():
                            messagebox.showinfo("Success", f"Student {sname} has been deleted successfully!")
                            search_students()  # Refresh list
                        else:
                            messagebox.showerror("Error", "Failed to save changes to file")
                
                ctk.CTkButton(
                    card,
                    text="🗑️ Delete",
                    font=("Arial", 12, "bold"),
                    fg_color="#ef4444",
                    hover_color="#dc2626",
                    corner_radius=8,
                    width=100,
                    height=35,
                    command=delete_student
                ).place(relx=0.98, rely=0.5, anchor="e")
        
        ctk.CTkButton(
            search_container,
            text="🔍 Search",
            font=("Arial", 13, "bold"),
            fg_color="#6366f1",
            hover_color="#4f46e5",
            corner_radius=8,
            width=100,
            height=40,
            command=search_students
        ).pack(side="left", padx=5)
        
        # Initial display
        search_students()

    def show_update_student(self):
        """Update student view"""
        self.clear_content_display()
        self.page_title_label.configure(text="✏️ Update Student Record")
        
        if not self.student_data['records']:
            ctk.CTkLabel(
                self.content_display_frame,
                text="No student records found!",
                font=("Arial", 16),
                text_color="#64748b"
            ).pack(pady=50)
            return
        
        # Student selection
        selection_frame = ctk.CTkFrame(self.content_display_frame, fg_color="#f8fafc", corner_radius=15, border_width=2, border_color="#e2e8f0", height=150)
        selection_frame.pack(fill="x", pady=(0, 20))
        selection_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            selection_frame,
            text="Select Student to Update",
            font=("Arial", 18, "bold"),
            text_color="#1e293b"
        ).pack(pady=15)
        
        student_names = [f"{record['name']} ({sid})" for sid, record in self.student_data['records'].items()]
        
        student_dropdown = ctk.CTkComboBox(
            selection_frame,
            values=student_names,
            font=("Arial", 13),
            width=400,
            height=40,
            corner_radius=8,
            border_width=2,
            border_color="#e2e8f0"
        )
        student_dropdown.set(student_names[0] if student_names else "")
        student_dropdown.pack()
        
        # Update form frame
        form_frame = ctk.CTkScrollableFrame(self.content_display_frame,height=500, fg_color="transparent")
        form_frame.pack(fill="both", expand=True)
        
        def load_student_data():
            for widget in form_frame.winfo_children():
                widget.destroy()
            
            selected = student_dropdown.get()
            if not selected:
                return
            
            student_id = selected.split('(')[-1].strip(')')
            record = self.student_data['records'][student_id]
            stats = self.calculate_student_statistics(record)
            
            # Info card
            info_card = ctk.CTkFrame(form_frame, fg_color="#f8fafc", corner_radius=15, border_width=2, border_color="#e2e8f0")
            info_card.pack(fill="x", pady=(0, 20))
            
            ctk.CTkLabel(
                info_card,
                text=f"Current Stats: {stats['percentage']:.1f}% | Grade: {stats['grade']}",
                font=("Arial", 16, "bold"),
                text_color="#6366f1"
            ).pack(pady=15)
            
            # Edit form
            edit_frame = ctk.CTkFrame(form_frame, fg_color="#f8fafc", corner_radius=15, border_width=2, border_color="#e2e8f0")
            edit_frame.pack(fill="both", expand=True)
            
            ctk.CTkLabel(
                edit_frame,
                text="Update Information",
                font=("Arial", 18, "bold"),
                text_color="#1e293b"
            ).pack(pady=20)
            
            fields_container = ctk.CTkFrame(edit_frame, fg_color="transparent")
            fields_container.pack(pady=20, padx=40, fill="x")
            
            entries = {}
            fields = [
                ("Student Name", "name", record['name']),
                ("Coursework 1 (0-20)", "cw1", str(record['coursework_1'])),
                ("Coursework 2 (0-20)", "cw2", str(record['coursework_2'])),
                ("Coursework 3 (0-20)", "cw3", str(record['coursework_3'])),
                ("Exam Mark (0-100)", "exam", str(record['exam_mark']))
            ]
            
            for label, key, default_val in fields:
                field_frame = ctk.CTkFrame(fields_container, fg_color="transparent")
                field_frame.pack(fill="x", pady=10)
                
                ctk.CTkLabel(
                    field_frame,
                    text=label,
                    font=("Arial", 13, "bold"),
                    text_color="#1e293b",
                    width=200,
                    anchor="w"
                ).pack(side="left")
                
                entry = ctk.CTkEntry(
                    field_frame,
                    font=("Arial", 13),
                    width=300,
                    height=40,
                    corner_radius=8,
                    border_width=2,
                    border_color="#e2e8f0"
                )
                entry.insert(0, default_val)
                entry.pack(side="left", padx=20)
                entries[key] = entry
            
            status_label = ctk.CTkLabel(
                edit_frame,
                text="",
                font=("Arial", 12)
            )
            status_label.pack(pady=10)
            
            def update_student():
                try:
                    new_name = entries['name'].get().strip()
                    cw1 = int(entries['cw1'].get().strip())
                    cw2 = int(entries['cw2'].get().strip())
                    cw3 = int(entries['cw3'].get().strip())
                    exam = int(entries['exam'].get().strip())
                    
                    if not new_name:
                        status_label.configure(text="❌ Name cannot be empty", text_color="#ef4444")
                        return
                    
                    if not (0 <= cw1 <= 20 and 0 <= cw2 <= 20 and 0 <= cw3 <= 20):
                        status_label.configure(text="❌ Coursework marks must be between 0-20", text_color="#ef4444")
                        return
                    
                    if not (0 <= exam <= 100):
                        status_label.configure(text="❌ Exam mark must be between 0-100", text_color="#ef4444")
                        return
                    
                    # Update record
                    self.student_data['records'][student_id] = {
                        'name': new_name,
                        'student_number': student_id,
                        'coursework_1': cw1,
                        'coursework_2': cw2,
                        'coursework_3': cw3,
                        'exam_mark': exam
                    }
                    
                    if self.save_to_file():
                        status_label.configure(text="✅ Student updated successfully!", text_color="#10b981")
                        messagebox.showinfo("Success", f"Student {new_name} has been updated successfully!")
                        
                        # Refresh dropdown
                        student_names = [f"{r['name']} ({sid})" for sid, r in self.student_data['records'].items()]
                        student_dropdown.configure(values=student_names)
                        
                        load_student_data()
                    else:
                        status_label.configure(text="❌ Failed to save to file", text_color="#ef4444")
                
                except ValueError:
                    status_label.configure(text="❌ Please enter valid numbers for marks", text_color="#ef4444")
            
            buttons_frame = ctk.CTkFrame(edit_frame, fg_color="transparent")
            buttons_frame.pack(pady=20)
            
            ctk.CTkButton(
                buttons_frame,
                text="✅ Save Changes",
                font=("Arial", 14, "bold"),
                fg_color="#10b981",
                hover_color="#059669",
                corner_radius=10,
                width=150,
                height=45,
                command=update_student
            ).pack(side="left", padx=10)
            
            ctk.CTkButton(
                buttons_frame,
                text="🔄 Reset",
                font=("Arial", 14, "bold"),
                fg_color="#64748b",
                hover_color="#475569",
                corner_radius=10,
                width=150,
                height=45,
                command=load_student_data
            ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            selection_frame,
            text="📝 Load Student",
            font=("Arial", 13, "bold"),
            fg_color="#6366f1",
            hover_color="#4f46e5",
            corner_radius=8,
            width=120,
            height=40,
            command=load_student_data
        ).pack(pady=(5, 15))
        
        # Initial load
        load_student_data()


# --- MAIN FUNCTION ---
def main():
    """Main function to run the application - creates CTk and starts mainloop."""
    root_window = ctk.CTk()
    app = StudentManagerApp(root_window)
    root_window.mainloop()


if __name__ == "__main__":
    main()