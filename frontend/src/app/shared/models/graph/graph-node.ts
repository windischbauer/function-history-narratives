export class GraphNode {
  id?: string | number;
  label?: string | number;

  constructor(id?: string | number, label?: string | number) {
    if (id) {
      this.id = id;
    }
    if (label) {
      this.label = label;
    }
  }

}
