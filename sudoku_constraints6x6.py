init = ['C11', 'C12', 'C13', 'C14', 'C15', 'C16', 
        'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 
        'C31', 'C32', 'C33', 'C34', 'C35', 'C36', 
        'C41', 'C42', 'C43', 'C44', 'C45', 'C46', 
        'C51', 'C52', 'C53', 'C54', 'C55', 'C56', 
        'C61', 'C62', 'C63', 'C64', 'C65', 'C66']
constraints = [[1,2],[1,3],[1,4],[1,5],[1,6],
               [2,1],[2,3],[2,4],[2,5],[2,6],
               [3,1],[3,2],[3,4],[3,5],[3,6],
               [4,1],[4,2],[4,3],[4,5],[4,6],
               [5,1],[5,2],[5,3],[5,4],[5,6],
               [6,1],[6,2],[6,3],[6,4],[6,5]]
squares = [['C11', 'C12', 'C13', 'C21', 'C22', 'C23'],
           ['C14', 'C15', 'C16', 'C24', 'C25', 'C26'],
           ['C31', 'C32', 'C33', 'C41', 'C42', 'C43'],
           ['C34', 'C35', 'C36', 'C44', 'C45', 'C46'],
           ['C51', 'C52', 'C53', 'C61', 'C62', 'C63'],
           ['C54', 'C55', 'C56', 'C64', 'C65', 'C66']]
constraint6x6 = {}
for i in range(36):
    for j in range(len(init)):
        if init[0] != init[j]:
            if init[0][1] == init[j][1] or init[0][2] == init[j][2]:
                constraint6x6[(init[0],init[j])] = constraints
            else:
                for square in squares:
                    if init[0] in square and init[j] in square:
                        constraint6x6[(init[0],init[j])] = constraints
    init.pop(0)