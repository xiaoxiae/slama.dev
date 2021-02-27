def menger(n, x, y, w, h):
  if n == 0:  # BASE CASE!
    return
  
  wn = w / 3
  hn = h / 3
  
  fill(255)
  rect(x + wn, y + hn, wn, hn)

  menger(n - 1, x, y, wn, hn)           # 1
  menger(n - 1, x + wn, y, wn, hn)      # 2
  menger(n - 1, x + 2 * wn, y, wn, hn)  # 3
  menger(n - 1, x, y + 2 * hn, wn, hn)           # 4
  menger(n - 1, x + wn, y + 2 * hn, wn, hn)      # 5
  menger(n - 1, x + 2 * wn, y + 2 * hn, wn, hn)  # 6
  menger(n - 1, x, y + hn, wn, hn)           # 7
  menger(n - 1, x + 2 * wn, y + hn, wn, hn)  # 8


def setup():
    size(400, 400)
    background(255)
    
def draw():
  fill(0)
  rect(0, 0, width, height)
  menger(5, 0, 0, width, height)
