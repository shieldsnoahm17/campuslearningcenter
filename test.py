import docx

# Define a list of course sets (course ID and time)
course_sets = [
    {'course_id': 'CS101', 'time': '10:00am - 12:00pm'},
    {'course_id': 'EN101', 'time': '1:00pm - 3:00pm'},
    {'course_id': 'MA201', 'time': '9:00am - 11:00am'},
    {'course_id': 'PH301', 'time': '2:00pm - 4:00pm'}
]

# Create a new Word document
document = docx.Document()

# Add a table with headers
table = document.add_table(rows=1, cols=2)
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Course ID'
hdr_cells[1].text = 'Time'

# Add rows to the table for each course set
for course_set in course_sets:
    row_cells = table.add_row().cells
    row_cells[0].text = course_set['course_id']
    row_cells[1].text = course_set['time']

# Save the document
document.save('course_schedule.docx')
