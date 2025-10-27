class FeedbackForm:
    def __init__(self):
        print("Welcom to Project 5 - Feedback Form")
        self.details = []
        
    def username(self, name:str):
        # name = input("Enter your name: ")
        self.details.append(name)
        return self.details
    
    def contact(self, email:str):
        # email = input("Enter your email: ")
        self.details.append(email)
        return self.details
    
    def feedback(self, feed):
        # feed = input("Enter your feedback: ")
        self.details.append(feed)
        return self.details
    
    def view_form(self):
        return self.details
        
        
if __name__=="__main__":
    feed = FeedbackForm()
    # print(feed.username("Saurabh"))
    # print(feed.contact("xyz@gmail.com"))
    # print(feed.feedback("It's a good experience."))