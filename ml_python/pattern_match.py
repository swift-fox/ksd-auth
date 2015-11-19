import Database

class PatternMatch:
    def compare_patterns(new_pat, old_pats):
        pass

    def register_user(username, password):
        db = Database()
        db.add_user(username, password)

    def compute_pattern(self, username, password, new_pat):
        db = Database()
        if db.exist_user() == False:
            pass # return authentication failed message

        old_pats = db.read_patterns(username)
        if self.compare_patterns(new_pat, old_pats) == True:
            db.add_pattern(username, new_pat)
        else:
            pass # return invalid pattern
