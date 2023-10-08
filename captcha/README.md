# Captcha 驗證
高科 Webp（校務系統）的人機驗證由四個英數文字組成，並且無大小寫之分。

## Requirements
Python 3.11.2
| Package       | Version  | 備註 |
|---------------|----------|------|
| Pillow        | 10.0.1   |      |
| matplotlib    | 3.8.0    |      |
| numpy         | 1.26.0   |      |
| opencv-python | 4.8.1.78 |      |
| requests      | 2.31.0   |      |
| urllib3       | 2.0.5    |      |

## 已知問題
+ 當兩個文字過於靠近，OpenCV 會將他們框選在一起。
+ 有時二值化無法完全去除背景的躁點（會導致程式碼出錯）
