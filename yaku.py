from typing import List, Dict, Tuple
from utils import Tile, is_triplet, is_sequence, is_kong, recursive_tuple
from itertools import combinations, chain

T = Tile.from_str

'''
对于同时依赖多种状态输入的，应在UI层面确保输入无矛盾
'''

# 牌山 (包括副露，故可能多于14张)
_tiles: Tuple[Tile] = ()
# 副子 (_closed_melds + _open_melds)
_melds: Tuple[Tuple[Tile]] = ()
# 未副露副子
_closed_melds: Tuple[Tuple[Tile]] = ()
# 副露副子
_open_melds: Tuple[Tile] = ()
# 对子
_pair: Tuple[Tile] = ()
# 荣牌
_final_tile: Tile = T('east')
# 荣牌所在副子/对子 (只有可能是非副露的副子)
_final_meld_or_pair: Tuple[Tile] = ()

# 自风
_seat_wind: Tile = T('east')
# 场风
_round_wind: Tile = T('east')
# 栄和 (xor is_is_tsumohou)
_is_ronhou = False
# 自摸和 (xor _is_ronhou)
_is_tsumohou = False

# 立直 (-> _is_closed)
_is_riichi_: bool = False
# 一発 (-> is_riichi)
_is_ippatsu_: bool = False
# 最后一张
_is_last_draw: bool = False
# 嶺上開花 (-> kang in melds_without_final)
_is_rinshan_kaihou_: bool = False
# 抢杠 (-> _tiles.count(_final_tile) == 1 and _is_ronhou)
_is_chankan_: bool = False
# 両立直 (-> _is_closed and no_kang)
_is_double_riichi_: bool = False

# 天和
_is_tenhou_: bool = False
# 地和
_is_chiihou_: bool = False
# 流し満貫
_is_nagashi_mangan_: bool = False

# 匹配所有符合的番型
def get_all_yaku(
        final_tile: Tile,                           # 荣牌
        final_meld_or_pair: List[Tile],             # 荣牌所在副子/雀头
        tiles: List[Tile],                          # 牌山 (>= 14)
        closed_melds: List[List[Tile]] = (),        # 未副露副子
        open_melds: List[List[Tile]] = (),          # 副露副子
        pair: List[Tile] = (),                      # 雀头
        seat_wind: Tile = T('east'),                # 自风
        round_wind: Tile = T('east'),               # 场风
        is_ronhou: bool = True,                     # 荣和
        is_tsumohou: bool = False,                  # 自摸和
        is_riichi_: bool = False,                   # 立直
        is_ippatsu_: bool = False,                  # 一发
        is_last_draw: bool = False,                 # 最后一摸
        is_rinshan_kaihou_: bool = False,           # 岭上开花
        is_chankan_: bool = False,                  # 抢杠
        is_double_riichi_: bool = False,            # 双立直
        ):

    # global configuration
    _input(
        final_tile, final_meld_or_pair, tiles, closed_melds, open_melds, pair, seat_wind, round_wind, is_ronhou, 
        is_tsumohou, is_riichi_, is_ippatsu_, is_last_draw, is_rinshan_kaihou_, is_chankan_, is_double_riichi_
    )

    yalu_names = [yaku_name for yaku_name, is_yaku_valid in yaku_list.items() if is_yaku_valid()]

    # check conflicts between yakus
    # ...

    yalu_names_cn = [yaku_name_dict_cn[yaku_name] for yaku_name in yalu_names]
    return yalu_names_cn


# 更新全局状态
def _input(
        final_tile: Tile,                           # 荣牌
        final_meld_or_pair: List[Tile],             # 荣牌所在副子/雀头
        tiles: List[Tile],                          # 牌山 (>= 14)
        closed_melds: List[List[Tile]] = (),        # 未副露副子
        open_melds: List[List[Tile]] = (),          # 副露副子
        pair: List[Tile] = (),                      # 雀头
        seat_wind: Tile = T('east'),                # 自风
        round_wind: Tile = T('east'),               # 场风
        is_ronhou: bool = True,                     # 荣和
        is_tsumohou: bool = False,                  # 自摸和
        is_riichi_: bool = False,                   # 立直
        is_ippatsu_: bool = False,                  # 一发
        is_last_draw: bool = False,                 # 最后一摸
        is_rinshan_kaihou_: bool = False,           # 岭上开花
        is_chankan_: bool = False,                  # 抢杠
        is_double_riichi_: bool = False,            # 双立直
        ):
    global _tiles, _melds, _closed_melds, _open_melds, _pair, _final_tile, _final_meld_or_pair
    global _seat_wind, _round_wind, _is_ronhou, _is_tsumohou, _is_riichi_, _is_ippatsu_, _is_last_draw, _is_rinshan_kaihou_, _is_chankan_, _is_double_riichi_
    
    # pass information to global
    _closed_melds = closed_melds
    _open_melds = open_melds
    _tiles = tiles

    for meld in _closed_melds:
        meld.sort(key=lambda x: x.__repr__())
    for meld in _open_melds:
        meld.sort(key=lambda x: x.__repr__())
    _tiles.sort(key=lambda x: x.__repr__())

    _pair               = recursive_tuple(pair)
    _final_tile         = recursive_tuple(final_tile)
    _final_meld_or_pair = recursive_tuple(final_meld_or_pair)
    _melds              = recursive_tuple(_closed_melds + _open_melds)
    _closed_melds       = recursive_tuple(_closed_melds)
    _open_melds         = recursive_tuple(_open_melds)
    _tiles              = recursive_tuple(_tiles)

    _seat_wind          = seat_wind
    _round_wind         = round_wind
    _is_ronhou          = is_ronhou
    _is_tsumohou        = is_tsumohou
    _is_riichi_         = is_riichi_
    _is_ippatsu_        = is_ippatsu_
    _is_last_draw       = is_last_draw
    _is_rinshan_kaihou_ = is_rinshan_kaihou_
    _is_chankan_        = is_chankan_
    _is_double_riichi_  = is_double_riichi_

    # check conflict
    assert seat_wind in {T('east'), T('south'), T('west'), T('north')}
    assert round_wind in {T('east'), T('south'), T('west'), T('north')}
    assert is_ronhou != is_tsumohou
    assert not is_riichi_ or _is_closed()
    assert not is_ippatsu_ or is_riichi_
    assert not is_rinshan_kaihou_ or len([meld for meld in _melds if is_kong(meld) and meld != final_meld_or_pair]) > 0
    assert not is_double_riichi_ or not is_last_draw
    assert not is_chankan_ or _tiles.count(final_tile) == 1


# 門前清
def _is_closed():
    return len(_open_melds) == 0

## One han closed only

# Menzenchin tsumohou
# 「門前清自摸和」
# Closed only, Chiitoitsu accept
def _is_menzenchin_tsumohou():
    if not _is_closed():
        return False
    return _is_tsumohou


# Riichi
# 「立直」
# Closed only, Chiitoitsu accept
def _is_riichi():
    if not _is_closed():
        return False
    return _is_riichi_


# Ippatsu
# 「一発」
# Closed only, Chiitoitsu accept
def _is_ippatsu():
    if not _is_closed():
        return False
    return _is_ippatsu_


# Pinfu
# 「平和」
# Closed only, Chiitoitsu unaccept
def _is_pinfu():
    if not _is_closed():
        return False
    if False in [is_sequence(meld) for meld in _closed_melds]:
        return False
    if len(_pair) != 1:
        return False
    if _pair[0].type_ == 'dragon':
        return False
    if _pair[0] in [_seat_wind, _round_wind]:
        return False
    if not is_sequence(_final_meld_or_pair):
        return False
    if _final_meld_or_pair.index(_final_tile) == 1:
        return False
    return True



# Iipeikou
# 「一盃口」
# Closed only, Chiitoitsu unaccept
def _is_iipeikou():
    if not _is_closed():
        return False
    sequence_melds = tuple((meld for meld in _closed_melds if is_sequence(meld)))
    peikou_melds = {meld for meld in sequence_melds if sequence_melds.count(meld) >= 2}
    return len(peikou_melds) == 1


# One han


# Haitei raoyue
# 「海底撈月」
# May be open
def _is_haitei_raoyue():
    return _is_last_draw and _is_tsumohou


# Houtei raoyui
# 「河底撈魚」
# May be open
def _is_houtei_raoyui():
    return _is_last_draw and _is_ronhou


# Rinshan kaihou
# 「嶺上開花」
# May be open, Chiitoitsu unaccept
def _is_rinshan_kaihou():
    return _is_rinshan_kaihou_


# Chankan
# 「搶槓」
# May be open
def _is_chankan():
    return _is_chankan_


# Tanyao
# 「断幺九」
# May be open (Closed only on variation)
# Chiitoitsu accept
def _is_tanyao():
    for tile in _tiles:
        if tile.type_ not in {'characters', 'bamboo', 'dots'} or tile.idx in [1, 9]:
            return False
    return True



# Yakuhai
# 「役牌」
# May be open, Chiitoitsu unaccept
def _is_yakuhai(yakuhai):
    return len([meld[0] for meld in _melds if (is_triplet(meld) or is_kong(meld)) and meld[0] == yakuhai]) > 0

# 「役牌-發」
def _is_yakuhai_green(): 
    return _is_yakuhai(T('green'))

# 「役牌-中」
def _is_yakuhai_red():   
    return _is_yakuhai(T('red'))

# 「役牌-白」
def _is_yakuhai_white(): 
    return _is_yakuhai(T('white'))

# 「役牌-自风」
def _is_yakuhai_seat_wind(): 
    return _is_yakuhai(_seat_wind)

# 「役牌-场风」
def _is_yakuhai_round_wind(): 
    return _is_yakuhai(_round_wind)


# Two han


# Double riichi
# 「両立直」
# Closed only, Chiitoitsu accept
def _is_double_riichi():
    if not _is_closed():
        return False
    return _is_double_riichi_


# Chantaiyao
# 「全帯幺九」
# May be open (Loses 1 han), Chiitoitsu accept
def _is_chantaiyao():
    def is_taiyao(tiles): # 带幺九
        for tile in tiles:
            if tile.type_ in {'characters', 'bamboo', 'dots'} and tile.idx in {1, 9}:
                return True
            if tile.type_ in {'wind', 'dragon'}:
                return True
        return False

    if False in [is_taiyao(meld) for meld in list(_melds) + [_pair]]:
        return False
    return True


# Sanshoku doujun
# 「三色同順」
# May be open (Loses 1 han), Chiitoitsu unaccept
def _is_sanshoku_doujun():
    sequence_melds_head = [meld[0] for meld in _melds if is_sequence(meld)]
    if (len({meld.type_ for meld in sequence_melds_head}) < 3):
        return False
    for seq_comb in combinations(sequence_melds_head, 3):
        if len({seq.idx for seq in seq_comb}) == 1 and len({seq.type_ for seq in seq_comb}) == 3:
            return True
    return False
    


# Ittsu
# 「一気通貫」
# May be open (Loses 1 han), Chiitoitsu unaccept
def _is_ittsu():
    for type_ in {'characters', 'bamboo', 'dots'}:
        if (Tile(type_, idx=1), Tile(type_, idx=2), Tile(type_, idx=3)) in _melds and (Tile(type_, idx=4), Tile(type_, idx=5), Tile(type_, idx=6)) in _melds and (Tile(type_, idx=7), Tile(type_, idx=8), Tile(type_, idx=9)) in _melds:
            return True
    return False


# Toitoi
# 「対々」
# May be open, Chiitoitsu unaccept
def _is_toitoi():
    triplet_melds = [meld for meld in _melds if is_triplet(meld)]
    return len(triplet_melds) == 4


# Sanankou
# 「三暗刻」
# May be open, Chiitoitsu unaccept
def _is_sanankou():
    ankous = [meld for meld in _closed_melds if is_triplet(meld)]
    return len(ankous) == 3
    


# Sanshoku doukou
# 「三色同刻」
# May be open, Chiitoitsu unaccept
def _is_sanshoku_doukou():
    triplet_melds_head = [meld[0] for meld in _melds if is_triplet(meld)]
    if (len({meld.type_ for meld in triplet_melds_head}) < 3):
        return False
    for triplet_comb in combinations(triplet_melds_head, 3):
        if len({tri.idx for tri in triplet_comb}) == 1 and len({tri.type_ for tri in triplet_comb}) == 3:
            return True
    return False


# Sankantsu
# 「三槓子」
# May be open, Chiitoitsu unaccept
def _is_sankantsu():
    if len(_pair) == 0:
        return False
    kantsus = [meld for meld in _melds if is_kong(meld)]
    return len(kantsus) == 3


# Chiitoitsu
# 「七対子」
# Closed only
def _is_chiitoitsu():
    if not _is_closed():
        return False
    return len(_tiles) == 14 and _melds == [] and len(set(_tiles)) == 7 and _tiles[0::2] == _tiles[1::2]


# Honroutou
# 「混老頭」
# May be open (Consider as 4 han †), Chiitoitsu accept
def _is_honroutou():
    is_tile_houroutou = lambda tile: (tile.type_ in {'characters', 'bamboo', 'dots'} and tile.idx in {1, 9}) or tile.type_ in {'wind', 'dragon'}
    if False in [is_tile_houroutou(tile) for tile in _tiles]:
        return False
    return True


# Shousangen
# 「小三元」
# May be open (Consider as 4 han †), Chiitoitsu unaccept
def _is_shousangen():
    if len(_pair) == 0 or len(_melds) == 0:
        return False
    dragon_triplet_melds = [meld for meld in _melds if is_triplet(meld) and meld[0].type_ == 'dragon']
    return len(dragon_triplet_melds) == 2 and len(_pair[0]) == 1 and _pair[0].type_ == 'dragon'


# Three han


# Honitsu
# 「混一色」
# May be open (Loses 1 han), Chiitoitsu accept
def _is_honitsu():
    suit_tiles = [tile for tile in _tiles if tile.type_ in {'characters', 'bamboo', 'dots'}]
    honor_tiles = [tile for tile in _tiles if tile.type_ in {'wind', 'dragon'}]
    return len({tile.type_ for tile in suit_tiles}) == 1 and len(honor_tiles) > 0


# Junchan taiyao
# 「純全帯么」
# May be open (Loses 1 han), Chiitoitsu accept
def _is_junchan_taiyao():
    def is_jun_taiyao(tiles): # 全幺九
        for tile in tiles:
            if tile.type_ in {'characters', 'bamboo', 'dots'} and tile.idx in {1, 9}:
                return True
        return False

    if False in [is_jun_taiyao(meld) for meld in list(_melds) + [_pair]]:
        return False
    return True


# Ryanpeikou
# 「二盃口」
# Closed only, Chiitoitsu unaccept
def _is_ryanpeikou():
    if len(_pair) == 0 or len(_melds) == 0:
        return False
    if not _is_closed():
        return False
    sequence_melds = [meld for meld in _closed_melds if is_sequence(meld)]
    peikou_melds = {meld for meld in sequence_melds if sequence_melds.count(meld) >= 2}
    return len(peikou_melds) == 2


# Six han


# Chinitsu
# 「清一色」
# May be open (Loses 1 han), Chiitoitsu accept
def _is_chinitsu():
    suit_tiles = [tile for tile in _tiles if tile.type_ in {'characters', 'bamboo', 'dots'}]
    honor_tiles = [tile for tile in _tiles if tile.type_ in {'wind', 'dragon'}]
    return len({tile.type_ for tile in suit_tiles}) == 1 and len(honor_tiles) == 0


# Yakuman


# Kazoe yakuman
# 「数え役満」
# May be open
def _is_kazoe_yakuman():
    pass


# Kokushi musou
# 「国士無双 or 国士無双１３面待ち」
# Closed only
def _is_kokushi_musou():
    if not _is_closed():
        return False
    kokushi_musou = {
        T(str) for str in {
            '1s', '9s', '1w', '9w', '1p', '9p', 
            'east', 'south', 'west', 'north', 
            'green', 'red', 'white'
        }
    }
    return len(_tiles) == 14 and set(_tiles) == kokushi_musou


# Suuankou
# 「四暗刻 or 四暗刻単騎」
# Closed only, Chiitoitsu unaccept
def _is_suuankou():
    if not _is_closed:
        return False
    ankous = [meld for meld in _closed_melds if is_triplet(meld)]
    return len(ankous) == 4


# Daisangen
# 「大三元」
# May be open, Chiitoitsu unaccept
def _is_daisangen():
    dragon_triplet_melds = [meld for meld in _melds if is_triplet(meld) and meld[0].type_ == 'dragon']
    return len(dragon_triplet_melds) == 3


# Shousuushii
# 「小四喜」
# May be open, Chiitoitsu unaccept
def _is_shousuushii():
    wind_triplet_melds = [meld for meld in _melds if is_triplet(meld) and meld[0].type_ == 'wind']
    return len(wind_triplet_melds) == 3 and len(_pair) == 1 and _pair[0].type_ == 'wind'


# Daisuushii
# 「大四喜」
# May be open, Chiitoitsu unaccept
def _is_daisuushii():
    wind_triplet_melds = [meld for meld in _melds if is_triplet(meld) and meld[0].type_ == 'wind']
    return len(wind_triplet_melds) == 4


# Tsuuiisou
# 「字一色」
# May be open, Chiitoitsu unaccept
def _is_tsuuiisou():
    return len([tile for tile in _tiles if tile.type_ not in {'dragon', 'wind'}]) == 0


# Chinroutou
# 「清老頭」
# May be open, Chiitoitsu accept
def _is_chinroutou():
    is_tile_chinroutou = lambda tile: (tile.type_ in {'characters', 'bamboo', 'dots'} and tile.idx in {1, 9})
    if False in [is_tile_chinroutou(tile) for tile in _tiles]:
        return False
    return True


# Ryuuiisou
# 「緑一色」
# May be open
def _is_ryuuiisou():
    ryuu_tiles = {T(str) for str in {'2s', '3s', '4s', '6s', '8s', 'green'}}
    return len([tile for tile in _tiles if tile not in ryuu_tiles]) == 0


# Chuuren poutou
# 「九連宝燈 or 純正九蓮宝燈」
# Closed only
def _is_chuuren_poutou():
    if not _is_closed:
        return False
    suit_tiles = [tile for tile in _tiles if tile.type_ in {'characters', 'bamboo', 'dots'}]
    honor_tiles = [tile for tile in _tiles if tile.type_ in {'wind', 'dragon'}]
    if len(honor_tiles) != 0 or len({tile.type_ for tile in suit_tiles}) != 0:
        return False
    idxs = [tile.idx for tile in suit_tiles]
    return idxs == [3, 1, 1, 1, 1, 1, 1, 1, 3]


# Suukantsu
# 「四槓子」
# May be open
def _is_suukantsu():
    return len([meld for meld in _melds if is_kong(meld)]) == 4


# Initial yakuman


# Tenhou
# 「天和」
# Closed only
def _is_tenhou():
    return _is_tenhou_


# Chiihou
# 「地和」
# Closed only
def _is_chiihou():
    return _is_chiihou_


# Special case


# Nagashi mangan
# 「流し満貫」
# Closed only
def _is_nagashi_mangan():
    return _is_nagashi_mangan_


# Sepcial case (for export)

# Kokushi musou
# 「国士無双 or 国士無双１３面待ち」
def is_kokushi_musou(tiles):
    kokushi_musou = {
        T(str) for str in {
            '1s', '9s', '1w', '9w', '1p', '9p', 
            'east', 'south', 'west', 'north', 
            'green', 'red', 'white'
        }
    }
    return len(tiles) == 14 and set(tiles) == kokushi_musou

# Chiitoitsu
# 「七対子」
def is_chiitoitsu(tiles):
    return len(tiles) == 14 and len(set(tiles)) == 7 and tiles[0::2] == tiles[1::2]



# list
yaku_list = {
    'menzenchin_tsumohou': _is_menzenchin_tsumohou, 
    'riichi': _is_riichi, 
    'ippatsu': _is_ippatsu, 
    'pinfu': _is_pinfu, 
    'iipeikou': _is_iipeikou, 
    'haitei_raoyue': _is_haitei_raoyue, 
    'houtei_raoyui': _is_houtei_raoyui, 
    'rinshan_kaihou': _is_rinshan_kaihou, 
    'chankan': _is_chankan, 
    'tanyao': _is_tanyao, 
    'is_yakuhai_green': _is_yakuhai_green, 
    'is_yakuhai_red': _is_yakuhai_red, 
    'is_yakuhai_white': _is_yakuhai_white, 
    'is_yakuhai_seat_wind': _is_yakuhai_seat_wind, 
    'is_yakuhai_round_wind': _is_yakuhai_round_wind, 
    'double_riichi': _is_double_riichi, 
    'chantaiyao': _is_chantaiyao, 
    'sanshoku_doujun': _is_sanshoku_doujun, 
    'ittsu': _is_ittsu, 
    'toitoi': _is_toitoi, 
    'sanankou': _is_sanankou, 
    'sanshoku_doukou': _is_sanshoku_doukou, 
    'sankantsu': _is_sankantsu, 
    'chiitoitsu': _is_chiitoitsu, 
    'honroutou': _is_honroutou, 
    'shousangen': _is_shousangen, 
    'honitsu': _is_honitsu, 
    'junchan_taiyao': _is_junchan_taiyao, 
    'ryanpeikou': _is_ryanpeikou, 
    'chinitsu': _is_chinitsu, 
    'kazoe_yakuman': _is_kazoe_yakuman, 
    'kokushi_musou': _is_kokushi_musou, 
    'suuankou': _is_suuankou, 
    'daisangen': _is_daisangen, 
    'shousuushii': _is_shousuushii, 
    'daisuushii': _is_daisuushii, 
    'tsuuiisou': _is_tsuuiisou, 
    'chinroutou': _is_chinroutou, 
    'ryuuiisou': _is_ryuuiisou, 
    'chuuren_poutou': _is_chuuren_poutou, 
    'suukantsu': _is_suukantsu, 
    'tenhou': _is_tenhou, 
    'chiihou': _is_chiihou, 
    'nagashi_mangan': _is_nagashi_mangan, 
}

yaku_name_dict_cn = {
    'menzenchin_tsumohou': '门清自摸', 'riichi': '立直', 'ippatsu': '一发', 'pinfu': '平和', 'iipeikou': '一杯口', 
    'haitei_raoyue': '海底捞月', 'houtei_raoyui': '河底捞鱼', 'rinshan_kaihou': '岭上开花', 'chankan': '抢杠', 
    'tanyao': '断幺九', 'is_yakuhai_green': '役牌-發', 'is_yakuhai_red': '役牌-中', 'is_yakuhai_white': '役牌-白', 
    'is_yakuhai_seat_wind': '役牌-自风', 'is_yakuhai_round_wind': '役牌-场风', 'double_riichi': '两立直', 
    'chantaiyao': '全带幺九', 'sanshoku_doujun': '三色同顺', 'ittsu': '一气通贯', 'toitoi': '对对和', 'sanankou': '三暗刻', 
    'sanshoku_doukou': '三色同刻', 'sankantsu': '三杠子', 'chiitoitsu': '七对子', 'honroutou': '混老头', 
    'shousangen': '小三元', 'honitsu': '混一色', 'junchan_taiyao': '纯带幺九', 'ryanpeikou': '二杯口', 
    'chinitsu': '清一色', 'kazoe_yakuman': '累计役满', 'kokushi_musou': '国士无双', 'suuankou': '四暗刻', 
    'daisangen': '大三元', 'shousuushii': '小四喜', 'daisuushii': '大四喜', 'tsuuiisou': '字一色', 'chinroutou': '清老头', 
    'ryuuiisou': '绿一色', 'chuuren_poutou': '九莲宝灯', 'suukantsu': '四杠子', 'tenhou': '天和', 'chiihou': '地和', 
    'nagashi_mangan': '流局满贯', 
}

if __name__ == '__main__':
    T = T

    my_closed_melds = [
        [T('6s'), T('7s'), T('8s')], 
        [T('6p'), T('7p'), T('8p')], 
        [T('6w'), T('7w'), T('8w')], 
        [T('north'), T('north'), T('north')]
    ]
    my_open_melds = []
    my_pair = [T('7s'), T('7s')]
    my_final_tile = T('7s')
    my_final_meld_or_pair = [T('7s'), T('7s'),]
    my_tiles = list(chain(*(my_closed_melds + my_open_melds + [my_pair])))

    print(my_final_tile)
    print(my_final_meld_or_pair)
    print(my_closed_melds)
    print(my_open_melds)
    print(my_pair)

    yaku = get_all_yaku(my_final_tile, my_final_meld_or_pair, my_tiles, my_closed_melds, my_open_melds, my_pair)
    # print(yaku)

