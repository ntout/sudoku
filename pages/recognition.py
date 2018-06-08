import cv2
import os
from statistics import mode

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_in_image(image_file_path):
    return cv2.imread(image_file_path)


def find_puzzle(img):
    lists1 = []
    C, H, W = img.shape[::-1]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 205, 255, 0)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contours)):
        cnt = contours[i]
        perimeter = cv2.arcLength(cnt, True)
        if W <= perimeter <= W+W+H+H - 5:
            lists1.append(i)
            x, y, w, h = cv2.boundingRect(cnt)
            return img[y:y + h, x:x + w]


def resize_puzzle(puz):
    width = 451
    height = 451
    dim = (width, height)
    return cv2.resize(puz, dim, interpolation=cv2.INTER_AREA)


def bold_puzzle_lines(resized):
    yuBnd = 1
    ylBnd = 50
    x = 1
    for row in range(9):
        xlBnd = 1
        xrBnd = 50
        for col in range(9):
            cv2.rectangle(resized, (xlBnd, yuBnd), (xrBnd, ylBnd), (0, 0, 0), 3)
            xlBnd += 50
            xrBnd += 50
            x += 1
        yuBnd += 50
        ylBnd += 50


def find_puz_contours(bold_puz):
    C, H, W = bold_puz.shape[::-1]
    gray = cv2.cvtColor(bold_puz, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 100, 255, 0)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def filter_contours(contours):
    lists1 = []

    for i in range(len(contours)):
        perimeter = cv2.arcLength(contours[i], True)
        if 160 <= perimeter <= 175:
            lists1.append(i)
    return lists1


def extract_puz_numbers(resized, contours, list_contours):
    puzzle = {}
    square = 81
    for x in list_contours:
        m = cv2.moments(contours[x])
        cx = int(m['m10']/m['m00'])
        cy = int(m['m01']/m['m00'])
        cv2.rectangle(resized, (cx-20, cy-20), (cx+20, cy+20), (0, 255, 255), 1)
        cropped = resized[cy-20:cy+20, cx-20:cx+20]
        puzzle.update({square: {'val': 0, .9: [], .8: [], .7: []}})

        for eachNum in range(1, 10):
            for eachVer in range(1, 82):
                template = cv2.imread(os.path.join(BASE_DIR, 'media/train_img/numbers/{}.{}.png'.format(eachNum, eachVer)))
                result = cv2.matchTemplate(cropped, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if max_val > 0.9:
                    puzzle[square][.9].append(eachNum)
                if max_val > .8:
                    puzzle[square][.8].append(eachNum)
                if max_val > .7:
                    puzzle[square][.7].append(eachNum)
        square -= 1
    return puzzle


def determine_value(puzzle):
    puz_list = []
    for key in puzzle:
        if len(puzzle[key][.9]) > 0:
            puzzle[key]['val'] = mode(puzzle[key][.9])
        elif len(puzzle[key][.8]) > 0:
            puzzle[key]['val'] = mode(puzzle[key][.8])
        elif len(puzzle[key][.7]) > 0:
            puzzle[key]['val'] = mode(puzzle[key][.7])
        puz_list.append(str(puzzle[key]['val']))
    return puz_list


def list_to_str(lst):
    return ''.join(lst[::-1])


if __name__ == '__main__':
    pass
