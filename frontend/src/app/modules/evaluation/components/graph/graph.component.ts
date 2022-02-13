import { AfterViewInit, Component, ElementRef, Input, OnChanges, OnInit, ViewChild } from '@angular/core';
import { GraphService } from '@core/services/graph.service';


@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.scss'],
})
export class GraphComponent implements OnInit, AfterViewInit, OnChanges {
  @ViewChild('callgraph', {static: false})
  callgraph!: ElementRef;
  callgraphInstance: any;

  @Input() input: { nodes, edges };

  constructor(
    private graphService: GraphService,
  ) {
  }

  ngOnInit(): void {
  }

  ngOnChanges(): void {
    if (this.callgraphInstance) {
      this.drawGraph();
    }
  }

  ngAfterViewInit(): void {
    const container = this.callgraph;
    this.callgraphInstance = this.graphService.createNetwork(container);
    this.callgraphInstance.on('click', function(params) {
        const node = this.getNodeAt(params.pointer.DOM);
        document.getElementById('clickedNodeId').innerText = node;
      },
    );
    this.drawGraph();
  }

  drawGraph(): void {
    if (this.input) {
      this.callgraphInstance.setData(this.input);
    }
  }
}
