import argparse
import os
import cv2
import numpy as np

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--image", type=str, required=True, help="이미지 경로")
  args = parser.parse_args()

  gray = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
  if gray is None:
    print("사진 못 찾음!!!!!!1😜😜😜😜😜😜😜🥵🥵🥵🥵🥵🥵🥵")
    raise SystemExit(1)

  init_min = 100
  init_max = 200
  init_min = max(0, min(init_min, 500))
  init_max = max(init_min + 1, min(init_max, 500))

  win = "Canny Detection 상수값 조절하기"
  cv2.namedWindow(win, cv2.WINDOW_NORMAL)

  # 슬라이더바
  cv2.createTrackbar("Min", win, init_min, 500, lambda v: None)
  cv2.createTrackbar("Max", win, init_max, 500, lambda v: None)
  cv2.createTrackbar("Blur (odd)", win, 3, 31, lambda v: None)
  cv2.createTrackbar("L2grad (0/1)", win, 0, 1, lambda v: None)

  def compute_frame():
    # 현재 슬라이더바 값
    min_t = cv2.getTrackbarPos("Min", win)
    max_t = cv2.getTrackbarPos("Max", win)
    blur_k = cv2.getTrackbarPos("Blur (odd)", win)
    l2 = cv2.getTrackbarPos("L2grad (0/1)", win)

    # Max는 Min보다 커야 함 ㅇㅇ
    if max_t <= min_t:
      max_t = min_t + 1
      cv2.setTrackbarPos("Max", win, max_t)

    # 블러 커널은 홀수여야 함
    if blur_k < 1:
      blur_k = 1
    if blur_k % 2 == 0:
      blur_k += 1
      if blur_k > 31:
        blur_k = 31
      cv2.setTrackbarPos("Blur (odd)", win, blur_k)

    # blur + canny
    if blur_k > 1:
      blurred = cv2.GaussianBlur(gray, (blur_k, blur_k), 0)
    else:
      blurred = gray

    edges = cv2.Canny(blurred, min_t, max_t, L2gradient=bool(l2))

    # 이미지 표시
    left = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    right = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    vis = np.hstack([left, right])

    # 택스트
    status = f"Min:{min_t}  Max:{max_t}  Blur:{blur_k}  L2:{int(bool(l2))}   [S=Save  Q/ESC=Quit]"
    cv2.putText(vis, status, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow(win, vis)
    return edges, min_t, max_t

  while True:
    edges, min_t, max_t = compute_frame()
    key = cv2.waitKey(30) & 0xFF

    if key in (ord('q'), 27):  # q, ESC
      break
    if key == ord('s'):
      base = os.path.splitext(os.path.basename(args.image))[0]
      out = f"{base}_canny_{min_t}_{max_t}.png"
      cv2.imwrite(out, edges)
      print(f"저장 완료: {out}")

  cv2.destroyAllWindows()

if __name__ == "__main__":
  main()
