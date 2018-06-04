from django.shortcuts import render
from django.http import JsonResponse
import os
from pages.models import Puzzle, UploadedImage
from pages.sudoku import solver, string_to_array, array_to_string, create_sudoku, fill_blank_puzzle
from pages import recognition

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def home(request):
    return render(request, 'pages/index.html')


def intake(request):
    if request.method == 'POST':
        intake_string = request.POST.get('str')
        print(intake_string)
        if Puzzle.objects.filter(puzzle_blank=intake_string).exists():
            return JsonResponse({"puzzle": Puzzle.objects.filter(puzzle_blank=intake_string)[0].puzzle_solved})
        else:
            puzzle = Puzzle()
            arr = string_to_array(intake_string)
            arr_solved = solver(arr)
            solved_string = array_to_string(arr_solved)
            puzzle.puzzle_blank = intake_string
            puzzle.puzzle_solved = solved_string
            puzzle.save()
            return JsonResponse({"puzzle": solved_string})


def learn(request):
    if request.method == 'POST':
        n = request.POST.get('iterations')
        for i in range(n):
            solution = fill_blank_puzzle()
            new_puzzle = create_sudoku(solution)
            if not Puzzle.objects.filter(puzzle_solved=solution).exists():
                puzzle = Puzzle()
                puzzle.puzzle_blank = new_puzzle
                puzzle.puzzle_solved = solution
                puzzle.save()
        return JsonResponse({"puzzle": "done"})


def generate(request):
    if request.method == 'POST':
        fill_puzzle = fill_blank_puzzle()
        new_puzzle = create_sudoku(fill_puzzle)
        new_puzzle.replace('0', ' ')
        return JsonResponse({"puzzle": new_puzzle})


def helper(img):
    img2 = recognition.find_puzzle(img.file.path)
    resize = recognition.resize_puzzle(img2)
    recognition.bold_puzzle_lines(resize)
    cnt = recognition.find_puz_contours(resize)
    cnt_list = recognition.filter_contours(cnt)
    puzzle = recognition.extract_puz_numbers(resize, cnt, cnt_list)
    puzList = recognition.determine_value(puzzle)
    puzstr = recognition.list_to_str(puzList)
    return puzstr


def extract(request):
    if request.method == 'POST':
        img2 = recognition.find_puzzle(os.path.join(BASE_DIR, 'media', 'img', 'sud2.jpg'))
        resize = recognition.resize_puzzle(img2)
        recognition.bold_puzzle_lines(resize)
        cnt = recognition.find_puz_contours(resize)
        cnt_list = recognition.filter_contours(cnt)
        puzzle = recognition.extract_puz_numbers(resize, cnt, cnt_list)
        puzList = recognition.determine_value(puzzle)
        puzstr = recognition.list_to_str(puzList)
        return JsonResponse({"puzzle": puzstr})


def whatever(request):
    if request.method == 'POST':
        image = UploadedImage.objects.create(file=request.FILES.get('image'))
        # print(image.file.path)
        return JsonResponse({'puzzle': helper(image)})
