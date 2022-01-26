# 麻将算番工具
from typing import List, Dict
from utils import Tile, dedup
from yaku import get_all_yaku, is_kokushi_musou, is_chiitoitsu
from random import shuffle, sample

T = Tile.from_str

# 匹配3n+2
def _match_melds(tiles: List[Tile], melds: List[List[Tile]]=[], pair: List[Tile]=[]) -> List[Dict]:
    if len(tiles) == 0:
        return [{'melds': melds, 'pair': pair}]

    all_possible_melds = []
    tile = tiles[0]

    # match Sequence
    if tile.type_ in {'characters', 'bamboo', 'dots'} and tile.idx <= 7:
        if Tile(tile.type_, idx=tile.idx + 1) in tiles and Tile(tile.type_, idx=tile.idx + 2) in tiles:
            next_tiles = tiles.copy()
            next_meld = []
            for i in [0, 1, 2]:
                temp_tile = Tile(tile.type_, idx=tile.idx + i)
                next_tiles.remove(temp_tile)
                next_meld += [temp_tile]
            next_melds = melds + [next_meld]
            all_possible_melds += _match_melds(next_tiles, next_melds, pair)

    # match Triplet
    if tiles.count(tile) >= 3:
        next_tiles = tiles.copy()
        next_meld = []
        for i in range(3):
            next_tiles.remove(tile)
            next_meld += [tile]
        next_melds = melds + [next_meld]
        all_possible_melds += _match_melds(next_tiles, next_melds, pair)

    # match Pair
    if tiles.count(tile) >= 2 and len(pair) == 0:
        next_tiles = tiles.copy()
        next_pair = []
        for i in range(2):
            next_tiles.remove(tile)
            next_pair += [tile]
        all_possible_melds += _match_melds(next_tiles, melds, next_pair)

    return all_possible_melds

# 匹配3n+2
def get_all_possible_arrangements(tiles: List[Tile]=[]) -> List[Dict]:
    assert len(tiles) % 3 == 2
    # 排序，必要，后续操作均假定tiles已有序
    tiles.sort(key=lambda x: x.__repr__())
    all_possible_arrangements = []

    # 常规3+2匹配
    all_possible_arrangements += _match_melds(tiles=tiles, melds=[])
    # 国士无双匹配
    if is_kokushi_musou(tiles):
        all_possible_arrangements += [{'melds': [], 'pair': []}]
    # 七对子匹配
    if is_chiitoitsu(tiles):
        all_possible_arrangements += [{'melds': [], 'pair': []}]

    return all_possible_arrangements

# 快速测试
def quick_test(tiles: List[Tile]):
    shuffle(tiles)
    print('tiles:', tiles)
    print('ron-tile:', tiles[-1])
    final_tile = tiles[-1]
    arrangements = dedup(get_all_possible_arrangements(tiles))
    
    # 唯一不符合3n+2的，需要特判
    for arrangement in arrangements:
        print(arrangement)

        closed_melds = arrangement['melds']
        open_melds = []
        pair = arrangement['pair']

        final_meld_or_pairs = dedup([meld for meld in closed_melds + [pair] if final_tile in meld])
        if closed_melds == []:
            final_meld_or_pairs = [[]]
        for final_meld_or_pair in final_meld_or_pairs:
            print('ron-tile-meld/pair:', final_meld_or_pair)
            yaku_names = get_all_yaku(
                final_tile=final_tile,                      # 荣牌
                final_meld_or_pair=final_meld_or_pair,      # 荣牌所在副子/雀头
                tiles=tiles,                                # 牌山 (>= 14)
                closed_melds=closed_melds,                  # 未副露副子
                open_melds=open_melds,                      # 副露副子
                pair=pair,                                  # 雀头
            )
            print('yaku:', yaku_names)

    print()


if __name__ == '__main__':
    # quick_test([T(str) for str in '5s 4s green 9p white green 6s 9p white green 9p 3s 4s 5s'.split(' ')])
    # quick_test([T(str) for str in '2s 8p 2s 4p 9s 2s 6s 7s 8s 5p 8p 8p 9s 6p'.split(' ')])
    # quick_test([T(str) for str in '4p 4p 4p 5p 5p 5p 8s 8s 6s 6s 6s 3s 3s 3s'.split(' ')])
    # quick_test([T(str) for str in '3s 4s 5s 2s 3s 4s 8p 8p 5s 6s 7s 2p 3p 4p'.split(' ')])
    # quick_test([T(str) for str in '1p 2p 3p 1p 2p 3p 7s 8s 9s 5s 4s 3s red red'.split(' ')])
    
    # quick_test([T(str) for str in '2p 2p 3p 3p 4p 4p 6s 6s 7s 7s 8s 8s 5p 5p'.split(' ')])
    # quick_test([T(str) for str in '1s 2s 3s 7p 8p 9p green green green west west 9p 8p 7p'.split(' ')])
    # quick_test([T(str) for str in '1s 2s 3s 1w 2s 3w 1p 2p 3p 2s 3s 4s white white'.split(' ')])
    # quick_test([T(str) for str in '1s 2s 3s 2s 3s 4s 5s 5s 5s green green green west west'.split(' ')])
    # quick_test([T(str) for str in '1s 2s 3s 2s 3s 4s 4s 5s 6s 7s 8s 9s 4s 4s'.split(' ')])

    # quick_test([T(str) for str in '1s 1s 2s 2s 3s 3s 4s 4s 5s 5s 6s 6s 7s 7s'.split(' ')])
    # quick_test([T(str) for str in '1s 9s 1p 9p green green 1w 9w east north red west south white'.split(' ')])
    quick_test([T(str) for str in '1s 1s 1s 9p 9p 9p 9s 9s 9s 1w 1w 1w white white'.split(' ')])

