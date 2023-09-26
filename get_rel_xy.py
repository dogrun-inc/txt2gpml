# encoding: utf-8
import math

width = 150
height = 25

def main(startpoint:list, endpoint:list, start_rel=True, end_rel=True) -> dict:
    """_summary_
    interactionのstart, end二つのxy座標を引数に
    start_point, end_pointのx座標、y座標、RelX, RelYを返す
    各座標は引数の座標にノードの矩形のwidth, heightを加算した値となる

    Args
        startpoint: interactionのstart座標(x,y)
        endpoint: interactionのend座標()
        width: pathwayのwidth
        height: pathwayのheight
    
    Returns
        dict: start_pint xy座標、end_point xy座標、RelX, RelY
    """
    # start, end2点を結ぶ直線の傾きを求める
    s = { 'x': startpoint[0], 'y': startpoint[1] }
    e = { 'x': endpoint[0], 'y': endpoint[1] }

    # ラジアン単位を取得(radianの変換　n ×（π/180）)
    radian = math.atan2(e['y'] - s['y'], e['x'] - s['x'])
    #if 1.75*math.pi < radian or 0 < radian < 0.25*math.pi:
    if -0.75*math.pi <= radian < -0.25*math.pi:
        """
        start_pointはRelX=0, RelY=-1
        end_pointの座標はRexX=0, RelY=1
        """
        offset_start = height/2 if not start_rel else 0
        offset_end = height/2 if not end_rel else 0
        return {
            'start_point': {
                'x': s['x'],
                'y': s['y'] - offset_start,
                'RelX': 0,
                'RelY': -1 if start_rel else 0
            },
            'end_point': {
                'x': e['x'],
                'y': e['y'] + offset_end,
                'RelX': 0,
                'RelY': 1 if end_rel else 0
            }
        }
    elif -0.25*math.pi <= radian < 0.25*math.pi:
        """
        start_pointはRelX=1, RelY=0
        end_pointはRelX=-1, RelY=0
        """
        offset_start = width/2 if not start_rel else 0
        offset_end = width/2 if not end_rel else 0
        return {
            'start_point': {
                'x': s['x'] + offset_start,
                'y': s['y'],
                'RelX': 1,
                'RelY': 0
            },
            'end_point': {
                'x': e['x'] - offset_end,
                'y': e['y'],
                'RelX': -1  if end_rel else 0,
                'RelY': 0   
            }
        }

    elif 0.25*math.pi <= radian < 0.75*math.pi:
        """
        start_pointはRelX=0, RelY=1
        end_pointはRelX=0, RelY=-1
        """
        offset_start = height/2 if not start_rel else 0
        offset_end = height/2 if not end_rel else 0
        return {
            'start_point': {
                'x': s['x'],
                'y': s['y'] + offset_start,
                'RelX': 0,
                'RelY': 1 if start_rel else 0
            },
            'end_pooint': {
                'x': e['x'],
                'y': e['y'] - offset_end,
                'RelX': 0,
                'RelY': -1 if end_rel else 0
            }
        }
    elif 0.75*math.pi <= radian or radian < -0.75*math.pi:
        """
        start_pointはRelX=-1, RelY=0
        end_pointはRelX=1, RelY=0
        """
        offset_start = width/2 if not start_rel else 0
        offset_end = width/2 if not end_rel else 0
        return {
            'start_point': {
                'x': s['x'] - offset_start,
                'y': s['y'],
                'RelX': -1 if start_rel else 0,
                'RelY': 0
            },
            'end_point': {
                'x': e['x'] + offset_end,
                'y': e['y'],
                'RelX': 1 if end_rel else 0,
                'RelY': 0
            }   
        }

