from yaku import Tile
from main import quick_test

T = Tile.from_str

if __name__ == '__main__':
    T = Tile.from_str

    quick_test([T(str) for str in '5s 4s green 9p white green 6s 9p white green 9p 3s 4s 5s'.split(' ')])
    quick_test([T(str) for str in '2s 8p 2s 4p 9s 2s 6s 7s 8s 5p 8p 8p 9s 6p'.split(' ')])
    quick_test([T(str) for str in '4p 4p 4p 5p 5p 5p 8s 8s 6s 6s 6s 3s 3s 3s'.split(' ')])
    quick_test([T(str) for str in '3s 4s 5s 2s 3s 4s 8p 8p 5s 6s 7s 2p 3p 4p'.split(' ')])
    quick_test([T(str) for str in '1p 2p 3p 1p 2p 3p 7s 8s 9s 5s 4s 3s red red'.split(' ')])
    
    quick_test([T(str) for str in '2p 2p 3p 3p 4p 4p 6s 6s 7s 7s 8s 8s 5p 5p'.split(' ')])
    quick_test([T(str) for str in '1s 2s 3s 7p 8p 9p green green green west west 9p 8p 7p'.split(' ')])
    quick_test([T(str) for str in '1s 2s 3s 1w 2s 3w 1p 2p 3p 2s 3s 4s white white'.split(' ')])
    quick_test([T(str) for str in '1s 2s 3s 2s 3s 4s 5s 5s 5s green green green west west'.split(' ')])
    quick_test([T(str) for str in '1s 2s 3s 2s 3s 4s 4s 5s 6s 7s 8s 9s 4s 4s'.split(' ')])

    quick_test([T(str) for str in '1s 1s 2s 2s 3s 3s 4s 4s 5s 5s 6s 6s 7s 7s'.split(' ')])
    quick_test([T(str) for str in '1s 9s 1p 9p green green 1w 9w east north red west south white'.split(' ')])
    quick_test([T(str) for str in '1s 1s 1s 9p 9p 9p 9s 9s 9s 1w 1w 1w white white'.split(' ')])
