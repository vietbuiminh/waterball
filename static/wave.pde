/**
 * Sine Wave
 * by Daniel Shiffman.  
 * 
 * Render a simple sine wave. 
 */
 
int xspacing = 5;   // How far apart should each horizontal location be spaced
int w;              // Width of entire wave

float theta = 0.0;  // Start angle at 0
float amplitude = 20.0;  // Height of wave
float period = 300.0;  // How many pixels before the wave repeats
float dx;  // Value for incrementing X, a function of period and xspacing
float[] yvalues;  // Using an array to store height values for the wave

void setup() {
  divwidth = document.getElementById('indexhd').width;
  divheight = document.getElementById('indexhd').height;
  size(divwidth, divheight);
  colorMode(RGB, 255, 255, 255, 100);
  w = width+26;
  dx = (TWO_PI / period) * xspacing;
  yvalues = new float[w/xspacing];
}

void draw() {
  background(#758bfd);
  calcWave();
  renderWave();
}

void calcWave() {
  // Increment theta (try different values for 'angular velocity' here
  theta += 0.02;

  // For every x value, calculate a y value with sine function
  float x = theta;
  for (int i = 0; i < yvalues.length; i++) {
    yvalues[i] = cos(x)*amplitude;
    x+=dx;
  }
}

void renderWave() {
  noStroke();
  fill(255);
  // A simple way to draw the wave with an ellipse at each location
  for (int i = 0; i < 18; i++) {
    for (int x = 0; x < yvalues.length; x++) {
      ellipse(x*xspacing, (i*60)/2+yvalues[x], 2, 2);
    }
  }
}
