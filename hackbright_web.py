"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    try:
        # title, grade = hackbright.get_grades_by_github(github)
        rows = hackbright.get_grades_by_github(github)
        # return html

    except ValueError:
        return render_template('student_info.html', first=first, last=last, github=github)

    else:

        # return render_template('student_info.html', first=first, last=last, github=github, grade=grade, title=title)
        return render_template('student_info.html', student_info=rows, first=first, last=last, github=github)


    # return "{acct} is the GitHub account for {first} {last}".format(
    #     acct=github, first=first, last=last)


@app.route('/project/<title>')
def project_details(title):
    """ Lists information about a project. """

    title, description, max_grade = hackbright.get_project_by_title(title)

    names_and_grades = hackbright.get_names_and_grades_by_title(title)

    print names_and_grades

    return render_template('project-info.html', title=title, description=description, max_grade=max_grade,
                            ng=names_and_grades)



@app.route("/add-student")
def add_student():
    """Add a student."""

    return render_template("add-student.html")

# [(u'jhacks', u'Jane', u'Hacker', 2), (u'sdevelops', u'Sarah', u'Developer', 100)]


@app.route("/add-student", methods=['POST'])
def successfully_added():
    
    first_name = request.form.get('fname')
    last_name = request.form.get('lname')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template('successfully-added.html', github=github)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
