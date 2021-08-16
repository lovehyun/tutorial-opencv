import cv2
import numpy as np

display = True

def encrypt(img, msg, key):
    rows, cols = msg.shape[:2]
    enc = np.zeros((rows, cols, 3), np.uint8)

    print('Encrpyting...')
    for r in range(rows):
        for c in range(cols):
            for l in range(3):
                # turn them into 8-bit pixel values
                v1 = format(img[r,c,l], '08b')
                v2 = format(msg[r,c,l], '08b')

                # taking MSBs of each image
                v3 = v1[:key[0]] + v2[:key[1]]
                enc[r,c,l] = int(v3, base=2)

    if display:
        cv2.imshow('encrypted', enc)
        return enc
    else:
        cv2.imwrite('pics_enc.png', enc)

def decrypt(img, key):
    print('Decrypting...')
    if not display:
        # load encrypted image
        img = cv2.imread('pics_enc.png')

    rows, cols = img.shape[:2]

    img1 = np.zeros((rows, cols, 3), np.uint8)
    img2 = np.zeros((rows, cols, 3), np.uint8)

    for r in range(rows):
        for c in range(cols):
            for l in range(3):
                v1 = format(img[r,c,l], '08b')
                # get the MSB values and append with '0'
                v2 = v1[:key[0]] + '0' * key[1]
                v3 = v1[key[0]:] + '0' * key[0]

                # append data to img1 and img2
                img1[r,c,l]= int(v2, base=2)
                img2[r,c,l]= int(v3, base=2)

    if display:
        cv2.imshow('decrypted image', img1)
        cv2.imshow('decrypted message', img2)
    else:
        cv2.imwrite('img1_dec.png', img1)
        cv2.imwrite('img2_dec.png', img2)


if __name__ == "__main__":
    img = cv2.imread('../Resources/Photos/cats.jpg')
    msg = cv2.imread('../Resources/Photos/msg1.jpg')
    if display:
        cv2.imshow('original image', img)
        cv2.imshow('original message', msg)

    key = (7,1)
    enc = encrypt(img, msg, key)
    decrypt(enc, key)

    cv2.waitKey()
    cv2.destroyAllWindows()
