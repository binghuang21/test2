/* sniper */
/* strategy: since a scan of the entire battlefield can be done in 90 */
/* degrees from a corner, sniper can scan the field quickly. */

/* external variables, that can be used by any function */
var corner = 0;           /* current corner 0, 1, 2, or 2 */
var sc = 0;               /* current scan start */

var range;          /* range to target */

/* initialize the corner info */
/* x and y location of a corner, and starting scan degree */
var c1x = 2,  c1y = 2,  s1 = 0;
var c2x = 2,  c2y = 98, s2 = 270;
var c3x = 98, c3y = 98, s3 = 180;
var c4x = 98, c4y = 2,  s4 = 90;
var closest = Infinity;
new_corner();       /* start at a random corner */
var d = damage();       /* get current damage */
var dir = sc;           /* starting scan direction */

while (true) {         /* loop is executed forever */
  while (dir < sc + 90) {  /* scan through 90 degree range */
    range = scan(dir, 2);   /* look at a direction */
    if (range <= 70) {
      while (range > 0) {    /* keep firing while in range */
        closest = range;     /* set closest flag */
        cannon(dir, range);   /* fire! */
        range = scan(dir, 1); /* check target again */
        if (d + 15 > damage())  /* sustained several hits, */
          range = 0;            /* goto new corner */
      }
      dir -= 10;             /* back up scan, in case */
    }

    dir += 2;                /* increment scan */
    if (d != damage()) {     /* check for damage incurred */
      new_corner();          /* we"re hit, move now */
      d = damage();
      dir = sc;
    }
  }

  if (closest == Infinity) {       /* check for any targets in range */
    new_corner();             /* nothing, move to new corner */
    d = damage();
    dir = sc;
  } else {                     /* targets in range, resume */
    dir = sc;
  }
  closest = Infinity;
}

/* new corner function to move to a different corner */
function new_corner() {
  var x, y;

  var rand = Math.floor(Math.random() * 4);           /* pick a random corner */
  if (rand == corner)       /* but make it different than the */
    corner = (rand + 1) % 4;/* current corner */
  else
    corner = rand;
  if (corner == 0) {       /* set new x,y and scan start */
    x = c1x;
    y = c1y;
    sc = s1;
  }
  if (corner == 1) {
    x = c2x;
    y = c2y;
    sc = s2;
  }
  if (corner == 2) {
    x = c3x;
    y = c3y;
    sc = s3;
  }
  if (corner == 3) {
    x = c4x;
    y = c4y;
    sc = s4;
  }

  /* find the heading we need to get to the desired corner */
  var angle = plot_course(x,y);

  /* start drive train, full speed */

  /* keep traveling until we are within 15 meters */
  /* speed is checked in case we run into wall, other robot */
  /* not terribly great, since were are doing nothing while moving */

  while (distance(getX(), getY(), x, y) > 15)
    drive(angle, 100);

  /* cut speed, and creep the rest of the way */

  while (distance(getX(), getY(), x, y) > 1)
    drive(angle, 20);

  /* stop drive, should coast in the rest of the way */
  drive(angle, 0);
}  /* end of new_corner */

/* classical pythagorean distance formula */
function distance(x1, y1, x2, y2) {
  var x = x1 - x2;
  var y = y1 - y2;
  return Math.sqrt((x * x) + (y * y));
}

/* plot course function, return degree heading to */
/* reach destination x, y; uses atan() trig function */
function plot_course(xx, yy) {
  var d;
  var x,y;
  var curx, cury;

  curx = getX();  /* get current location */
  cury = getY();
  x = curx - xx;
  y = cury - yy;

  /* atan only returns -90 to +90, so figure out how to use */
  /* the atan() value */

  if (x == 0) {      /* x is zero, we either move due north or south */
    if (yy > cury)
      d = 90;        /* north */
    else
      d = 270;       /* south */
  } else {
    if (yy < cury) {
      if (xx > curx)
        d = 360 + Math.atan_deg(y / x);  /* south-east, quadrant 4 */
      else
        d = 180 + Math.atan_deg(y / x);  /* south-west, quadrant 3 */
    } else {
      if (xx > curx)
        d = Math.atan_deg(y / x);        /* north-east, quadrant 1 */
      else
        d = 180 + Math.atan_deg(y / x);  /* north-west, quadrant 2 */
    }
  }
  return d;
}