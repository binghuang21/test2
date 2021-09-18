/* counter */
/* scan in a counter-clockwise direction (increasing degrees) */
/* moves when hit */

var range;
var last_dir = 0;
/*参数说明:scan(angle, width)*/
var res = 2;
var d = damage();
var angle = Math.random() * 360;
while (true) {
  while ((range = scan(angle, res)) != Infinity) {
    if (range > 70) { /* out of range, head toward it */
      drive(angle, 50);
      var i = 1;
      while (i++ < 50) /* use a counter to limit move time */
        ;
      drive (angle, 0);
      if (d != damage()) {
        d = damage();
        run();
      }
      angle -= 3;
    } else {
      while (!cannon(angle, range))
        ;
      if (d != damage()) {
        d = damage();
        run();
      }
      angle -= 15;
    }
  }
  if (d != damage()) {
    d = damage();
    run();
  }
  angle += res;
  angle %= 360;
}

/* run moves around the center of the field */
function run() {
  var i = 0;
  var x = getX();
  var y = getY();

  if (last_dir == 0) {
    last_dir = 1;
    if (y > 51) {
      drive(270, 100);
      while (y - 10 < getY() && i++ < 50)
        ;
      drive(270, 0);
    } else {
      drive(90, 100);
      while (y + 10 > getY() && i++ < 50)
        ;
      drive(90, 0);
    }
  } else {
    last_dir = 0;
    if (x > 51) {
      drive(180, 100);
      while (x - 10 < getX() && i++ < 50)
        ;
      drive(180, 0);
    } else {
      drive(0, 100);
      while (x + 10 > getX() && i++ < 50)
        ;
      drive(0, 0);
    }
  }
}