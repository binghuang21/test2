/* rook.r  -  scans the battlefield like a rook, i.e., only 0,90,180,270 */
/* move horizontally only, but looks horz and vertically */

/* move to center of board */
if (getY() < 50) {
  while (getY() < 40)        /* stop near center */
    drive(90, 100);           /* start moving */
} else {
  while (getY() > 60)        /* stop near center */
    drive(270, 100);          /* start moving */
}
drive(0, 0);
while (speed() > 0)
  ;

/* initialize starting parameters */
var d = damage();
var course = 0;
var boundary = 99;
drive(course, 30);

/* main loop */
while(true) {
  /* look all directions */
  look(0);
  look(90);
  look(180);
  look(270);

  /* if near end of battlefield, change directions */
  if (course == 0) {
    if (getX() > boundary || speed() == 0)
      change();
  }
  else {
    if (getX() < boundary || speed() == 0)
      change();
  }
}

/* look somewhere, and fire cannon repeatedly at in-range target */
function look(deg) {
  var range;
  while ((range = scan(deg, 4)) <= 70)  {
    drive(course, 0);
    cannon(deg, range);
    if (d + 20 != damage()) {
      d = damage();
      change();
    }
  }
}

function change() {
  if (course == 0) {
    boundary = 1;
    course = 180;
  } else {
    boundary = 99;
    course = 0;
  }
  drive(course, 30);
}