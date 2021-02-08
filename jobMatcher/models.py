from jobMatcher import db


candidate_skill = db.Table('candidate_skill',
    db.Column('candidate_id', db.Integer, db.ForeignKey('candidate.id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id')),
)

job_skill = db.Table('job_skill',
    db.Column('job_id', db.Integer, db.ForeignKey('job.id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
)


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Skill %r>' % self.name


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    title = db.Column("job_id", db.String(80), db.ForeignKey('job.id'))
    skills = db.relationship('Skill', secondary=candidate_skill, backref="candidates", lazy="dynamic")

    def __repr__(self):
        return '<Candidate %r>' % self.name


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    skills = db.relationship('Skill', secondary=job_skill, backref="jobs", lazy="dynamic")
    candidates = db.relationship("Candidate", backref="job")

    def __repr__(self):
        return '<Job %r>' % self.title
