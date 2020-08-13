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

    def serialize(self):
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "link": self.link,
            "review": self.review,
            "salary": self.salary,
            "description": self.description
        }

    def from_json(self, json_):
        self.title = json_["title"]
        self.company = json_["company"]
        self.location = json_["location"]
        self.link = json_["link"]
        self.review = json_["review"]
        self.salary = json_["salary"]
        self.description = json_["description"]