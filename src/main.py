import copy

def readSudoku(filePath, lineNumber):
    with open(filePath) as f:
        lines = f.read().splitlines()
        return lines[lineNumber - 1]

def parseRawSudoku(sudokuRaw):
    sudoku = [[]]
    for char in sudokuRaw.strip():
        if len(sudoku[-1]) == 9:
            sudoku.append([])
        sudoku[-1].append(char)
    return sudoku

def printSudoku(parsedSudoku):
    for index, sudokuLine in enumerate(parsedSudoku):
        print(f'{" ".join(sudokuLine[0:3])} | {" ".join(sudokuLine[3:6])} | {" ".join(sudokuLine[6:9])}'.replace('.', '*'))
        if (index + 1) % 3 == 0 and index != 8:
            print('------+-------+------')

def getOptions(sudoku, row, col):
    rowFlags = [True for i in range(9)]
    for rowCol in range(9):
        value = sudoku[row][rowCol]
        if value != '.':
            parsedValue = int(value)
            rowFlags[parsedValue - 1] = False

    colFlags = [True for i in range(9)]
    for colRow in range(9):
        value = sudoku[colRow][col]
        if value != '.':
            parsedValue = int(value)
            colFlags[parsedValue - 1] = False

    cubeFlags = [True for i in range(9)]
    for cubeRow in range(3):
        for cubeCol in range(3):
            value = sudoku[int(row / 3) * 3 + cubeRow][int(col / 3) * 3 + cubeCol]
            if value != '.':
                parsedValue = int(value)
                cubeFlags[parsedValue - 1] = False

    optionFlags = [a and b and c for (a, b, c) in zip(rowFlags, colFlags, cubeFlags)]

    options = []
    for (index, optionFlag) in enumerate(optionFlags):
        if optionFlag:
            options.append(str(index + 1))

    return options

def solveSudoku(sudoku):
    sudokuCopy = copy.deepcopy(sudoku)
    options = copy.deepcopy(sudoku)
    numFilled = 1
    firstOptionsCoordsSet = False
    firstOptionsCoords = None
    while numFilled > 0:
        numFilled = 0
        firstOptionsCoordsSet = False
        for row in range(9):
            for col in range(9):
                if sudokuCopy[row][col] == '.':
                    currentOptions = getOptions(sudokuCopy, row, col)
                    if len(currentOptions) == 0:
                        return None
                    elif len(currentOptions) == 1:
                        sudokuCopy[row][col] = currentOptions[0]
                        options[row][col] = currentOptions[0]
                        numFilled += 1
                    else:
                        options[row][col] = currentOptions
                        if not firstOptionsCoordsSet:
                            firstOptionsCoordsSet = True
                            firstOptionsCoords = (row, col)

    if not firstOptionsCoordsSet:
        return sudokuCopy

    for option in options[firstOptionsCoords[0]][firstOptionsCoords[1]]:
        clonedSudoku = copy.deepcopy(sudokuCopy)
        clonedSudoku[firstOptionsCoords[0]][firstOptionsCoords[1]] = option
        solved = solveSudoku(clonedSudoku)
        if solved != None:
            return solved

    return None

SUDOKU_FILE_PATH = 'examples.txt'
SUDOKU_LINE_NUMBER = 4

def main():
    sudokuRaw = readSudoku(SUDOKU_FILE_PATH, SUDOKU_LINE_NUMBER)
    sudokuParsed = parseRawSudoku(sudokuRaw)
    print('Problem:')
    printSudoku(sudokuParsed)
    print()
    print('Solution:')
    solution = solveSudoku(sudokuParsed)
    if solution == None:
        print('No solution')
    else:
        printSudoku(solution)

main()
