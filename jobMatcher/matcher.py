from jobMatcher.models import Candidate, Job, Skill, db
import sys


class Matcher:
    def __init__(self, job_title, candidates=[]):
        self.job_title = job_title
        self.best_candidates = candidates

    def candidate_finder(self):
        if self._best_candidates_already_in_db():
            return
        # returns all the candidates in db with title=[self.job_title]
        candidates_list = Candidate.query.filter_by(title=self.job_title).all()
        # returns the skills list for job=[self.job_title]
        required_skills = Skill.query.join(Skill.jobs).filter_by(title=self.job_title).all()
        self._find_best_candidates(candidates_list, required_skills)
        self._save_candidates_for_this_job()

    def get_best_candidates(self):
        return self.best_candidates

    #save search results into DB for not having to search candidates again for this job next time
    def _save_candidates_for_this_job(self):
        job_ins = Job.query.filter_by(title=self.job_title).first()
        for candidate in self.best_candidates:
            candidate.job = job_ins
        db.session.commit()

    #find the best candidates who have as many [required_skills] as possible
    def _find_best_candidates(self, candidates, required_skills):
        if self.best_candidates:
            return self.best_candidates
        max_score = 0
        ideal_candidates = []
        for candidate in candidates:
            candidate_score = 0
            candidate_skills = Skill.query.join(Skill.candidates).filter_by(id=candidate.id).all()
            for skill in candidate_skills:
                if skill in required_skills:
                    candidate_score += 1
            # a better candidate score was found, initiate list with the correspond candidate
            if candidate_score > max_score:
                max_score = candidate_score
                ideal_candidates.clear()
                ideal_candidates.append(candidate)
            # candidate score is equal to current best score, add him to list
            elif candidate_score == max_score:
                ideal_candidates.append(candidate)
        self.best_candidates = ideal_candidates

    #check if best candidates for this job are already saved in DB
    def _best_candidates_already_in_db(self):
        ideal_candidates = Candidate.query.join(Candidate.job).filter_by(title=self.job_title).all()
        if ideal_candidates:
            self.best_candidates = ideal_candidates
            return True
        return False





