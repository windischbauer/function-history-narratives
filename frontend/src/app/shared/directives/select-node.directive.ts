import { Directive, EventEmitter, HostListener, Output } from '@angular/core';

@Directive({
  selector: '[appSelectNode]',
})
export class SelectNodeDirective {
  @Output() clickedNodeId: EventEmitter<number> = new EventEmitter<number>();
  clickedNode: HTMLElement;

  constructor() {
  }

  @HostListener('mousedown') onMouseDown(): void {
    this.clickedNode = document.getElementById('clickedNodeId');
    const id: number = +this.clickedNode.innerText;
    console.log(id);
    if (id) {
      this.emitClickedNodeId(id);
    }
  }

  emitClickedNodeId(id: number): void {
    this.clickedNodeId.emit(id);
  }
}
