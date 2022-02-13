import { ElementRef, Injectable } from '@angular/core';
import { Network, Options } from 'vis-network';
import { DataSet } from 'vis-data/peer/esm/vis-data';
import { GraphNode } from '@models/graph/graph-node';
import { GraphEdge } from '@models/graph/graph-edge';
import { BackendCommitService } from '@core/backend-services/backend-commit.service';

@Injectable({
  providedIn: 'root',
})
export class GraphService {

  constructor(
    private commitService: BackendCommitService,
  ) {
  }

  createNetwork(element: ElementRef, options?: Options): Network {
    const defaultOptions = {
      height: '100%',
      width: '100%',
      nodes: {
        shape: 'box',
        font: {
          color: 'white',
          face: 'monospace',
          align: 'left',
        },
      },
      clickToUse: false,
      edges: {
        smooth: false,
        arrows: {
          to: {
            enabled: true,
            type: 'arrow',
          },
        },
      },
      interaction: {
        multiselect: true,
      },
      layout: {
        hierarchical: {
          direction: 'LR',
          sortMethod: 'directed',
        },
      },
      physics: {
        hierarchicalRepulsion: {
          avoidOverlap: 1,
        },
      },
    };
    const network = new Network(element.nativeElement, {}, options || defaultOptions);
    return network;
  }

  transformData(data: any[], selectedVertexId: number | string): { nodes, edges } {
    // console.log('Transforming Data');
    const edges = new DataSet<any>();
    const tempNodes: GraphNode[] = [];
    const nodes = new DataSet<any>();

    data.forEach((e) => {
      // console.log(e.id);
      edges.add(new GraphEdge(e.id.toString(), e.from_, e.to_));
      const nodeFrom = {
        id: e.from_,
        label: e.from_name,
        color: {
          background: e.from_ === selectedVertexId ? '#D1495B' : '#124559',
          border: e.from_ === selectedVertexId ? '#a71f31' : '#003347',
          highlight: {
            border: '#ffd740',
            background: '#dbb835',
          },
        },
      };
      if (tempNodes.filter(n => n.id === nodeFrom.id).length === 0) {
        tempNodes.push(nodeFrom);
        nodes.add(nodeFrom);
      }
      const nodeTo = {
        id: e.to_,
        label: e.to_name,
        color: {
          background: e.to_ === selectedVertexId ? '#D1495B' : '#124559',
          border: e.to_ === selectedVertexId ? '#a71f31' : '#003347',
          highlight: {
            border: '#ffd740',
            background: '#dbb835',
          },
        },
      };
      if (tempNodes.filter(n => n.id === nodeTo.id).length === 0) {
        tempNodes.push(nodeTo);
        nodes.add(nodeTo);
      }
    });
    return {nodes, edges};
  }
}

// tslint:disable-next-line:max-line-length
// https://github.com/tillias/microservice-catalog/blob/8c4d42931fffc82c69a7f57207e47f6bfdc7677a/src/main/webapp/app/shared/vis/vis-network.service.ts#L8
