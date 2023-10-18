import React, { memo, useCallback } from 'react';
import { ConnectionLineComponent, Edge, getBezierPath, useStore, Position } from 'reactflow';
import { FlowEdge } from 'web_sd_shared_types/04_edge_t';
import { getEdgeParams } from '../logic/edge_utils';

const _PromptEdge = (elo: Edge<FlowEdge>) => {
    const sourceNode = elo.sourceNode
    const targetNode = elo.targetNode
    
    if (!sourceNode || !targetNode) {
        return null;
    }

    const { sx, sy, tx, ty, sourcePos, targetPos } = getEdgeParams(sourceNode, targetNode);

    const [edgePath] = getBezierPath({
      sourceX: sx as number,
      sourceY: sy as number,
      sourcePosition: sourcePos as Position,
      targetPosition: targetPos as Position,
      targetX: tx as number,
      targetY: ty as number,
      curvature: 0.2,
    });
    // console.log("edgePath: ", edgePath);

    return (
        <g>
            <path
                fill="none"
                stroke="#fff"
                strokeWidth={1.5}
                className="animated"
                d={edgePath}
            />
            {/* <circle cx={toX} cy={toY} fill="#fff" r={3} stroke="#222" strokeWidth={1.5} /> */}
        </g>
    );
};

export const PromptEdge = memo(_PromptEdge);
