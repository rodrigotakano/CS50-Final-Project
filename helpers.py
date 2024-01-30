def injection_check(input_string):
    chars = ["'", "-", " "]
    flag = 0
    for i in input_string:
        for j in chars:
            if i == j:
                flag = 1
                break
    if flag == 1:
        return False
    else:
        return True
    

class Add:
    def __init__(self, column_names):
        self.column_names = column_names        
    
    def placeholders(self):
        column_number = len(self.column_names)
        if column_number == 1:
            return '?'
        else:
            question_string = '?'
            for i in range(1, column_number):
                question_string = question_string + ',' + '?' 
            return question_string
        
    
    




    