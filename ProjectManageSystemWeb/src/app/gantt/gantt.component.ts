import {Component, OnInit, ViewChild} from '@angular/core';
import {DayPilot, DayPilotGanttComponent} from 'daypilot-pro-angular';

var tasks = [

  {
    "id": 1,
    "text": "项目管理系统",
    "complete": 35,
    "children": [
      {
        "id": 2,
        "start": "2019-09-04T00:00:00",
        "end": "2019-09-11T00:00:00",
        "text": "启动阶段",
        "complete": 60,
        "children": [
          {
            "id": 3,
            "start": "2019-09-04T00:00:00",
            "end": "2019-09-11T00:00:00",
            "text": "确立题目",
            "complete": 0
          },
        ]
      },
      {
        "id": 4,
        "start": "2019-09-11T00:00:00",
        "end": "2019-09-16T00:00:00",
        "text": "计划阶段",
        "complete": 0
      },
      {
        "id": 5,
        "start": "2019-09-16T00:00:00",
        "type": "Milestone",
        "text": "计划阶段完成",
        "end": "2019-09-16T00:00:00"
      }
    ],
    "start": "2019-09-04T00:00:00",
    "end": "2019-09-16T00:00:00"
  }
];

var links =  [
  {
    "from": 2,
    "to": 4,
    "type": "FinishToStart"
  }
];

var config = {
  autoRefreshEnabled: true,
  cellWidthSpec: "Fixed",
  cellWidth: 40,
  timeHeaders: [ { "groupBy": "Month", "format": "yyyy年MM月" },
    { "groupBy": "Day", "format": "d" }],
  heightSpec: "Parent100Pct",
  rowHeaderWidth: 150,
  scale: "Day",
  theme: "light",
  taskHeight: 30,
  rowHeaderHideIconEnabled: false,
  onRowClick: function(args) {
    console.info("onRowClick",args);
    console.info(this.tasks, this.links, this);
    this.selectedRows = [args.row.id];
    this.update();
  },
  onTaskClick: function(args) {
    console.info("onRowClick",args);
    console.info(this.tasks, this.links, this);
    this.selectedRows = [args.task.id()];
    this.update();
  },
  rowMoveHandling: "Update",
  onRowMoved: function (args) {
    console.info("onRowMoved",args);
    this.message("Row moved");
  },
  taskMoveHandling: "Update",
  onTaskMoved: function (args) {
    console.info("onTaskMoved",args);
    this.message("Task moved");
  },
  linkCreateHandling: "Disabled",
  rowCreateHandling: "Enabled",
  onRowCreate: function (args) {
    this.tasks.add(new DayPilot.Task({
      id: DayPilot.guid(),
      text: args.text,
      start: new DayPilot.Date().getDatePart(),
      end: new DayPilot.Date().getDatePart().addDays(1)
    }));
  },
  tasks,
  links
};

@Component({
  selector: 'app-gantt',
  templateUrl: './gantt.component.html',
  styleUrls: ['./gantt.component.css']
})

export class GanttComponent implements OnInit {

  constructor() { }

  ngOnInit() { }

  @ViewChild('gantt1', {static: false})

  gantt1: DayPilotGanttComponent;

  config: any = config;

}
