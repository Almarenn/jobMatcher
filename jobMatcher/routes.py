from jobMatcher import app, render_template, redirect, request, url_for, db
from jobMatcher.matcher import Matcher
from jobMatcher.models import Skill, Candidate, Job


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form["submit_button"] == "Load data":
            return redirect(url_for("load_data"))
        else:
            job_title = request.form["job"]
            #convert job_title to lower case
            job_in_lower = job_title.lower()
            job_ins = Job.query.filter_by(title=job_in_lower).first()
            if not job_ins:
                return f"<h1>No such job title, please try again</h1>"
            return redirect(url_for("candidate_finder", job_title=job_in_lower))
    else:
        return render_template("index.html")


@app.route('/<job_title>')
def candidate_finder(job_title):
    match = Matcher(job_title=job_title)
    match.candidate_finder()
    candidates_list = match.get_best_candidates()
    if not candidates_list:
        return f"<h1>No candidate was found for this job</h1>"
    else:
        return render_template("candidates_response.html", candidates=candidates_list)


#initiate db with skills, jobs and candidates
@app.route('/load_data')
def load_data():
    #db.drop_all()
    db.create_all()
    Candidate.query.delete()
    Job.query.delete()
    Skill.query.delete()
    skill1 = Skill(name="Java")
    skill2 = Skill(name="C++")
    skill3 = Skill(name="Python")
    skill4 = Skill(name="SQL")
    skills = [skill1, skill2, skill3, skill4]
    db.session.add_all(skills)
    db.session.commit()
    db.session.add_all([Job(title='software developer', skills=[skill1, skill2, skill3]),
                        Job(title='product manager', skills=[skill4]),
                        Job(title="qa engineer"),
                        Job(title="bookkeeper")]
                       )
    db.session.commit()
    db.session.add_all(
        [Candidate(name="Alex Doll", title="product manager", skills=[skill4]),
         Candidate(name="John Green", title="software developer", skills=[skill1, skill2]),
         Candidate(name="John Lennon", title="software developer", skills=[skill3, skill2]),
         Candidate(name="Paul Mcartney", title="software developer", skills=[skill3]),
         Candidate(name="George Harrison", title="qa engineer", skills=[skill3]),
         Candidate(name="Mac Miller", title="qa engineer")]
        )
    db.session.commit()
    return redirect(url_for("home"))