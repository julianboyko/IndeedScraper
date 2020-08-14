class Job:
    def __init__(self, title, company, location, link, review, salary):
        self.title = title
        self.company = company
        self.location = location
        self.link = link
        self.review = review
        self.salary = salary
        self.description = ""

    def add_description(self, description):
        self.description = description

    def get_title(self):
        return self.title

    def get_company(self):
        return self.company

    def get_location(self):
        return self.location

    def get_link(self):
        return self.link

    def get_review(self):
        return self.review

    def get_salary(self):
        return self.salary

    def get_description(self):
        return self.description