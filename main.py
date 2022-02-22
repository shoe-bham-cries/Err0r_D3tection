import pandas as pd


def binary(a):
    l, m = [], []
    for i in a:
        l.append(ord(i))
    for i in l:
        m.append(int(bin(i)[2:]))
    return m


def single_parity_generator(stream):
    parity = []
    flag = 0
    for digit in str(stream):
        flag += int(digit)
    if flag % 2 == 0:
        parity.append(0)
    else:
        parity.append(1)
    return parity


def single_parity_checker(stream):
    flag = 0
    for digit in stream:
        flag += int(digit)
    if flag % 2 == 0:
        print("No error detected")
    else:
        print("Error detected!")


def parity_generator(lists):
    parity = []
    for segment in lists:
        flag = 0
        for digit in str(segment):
            flag += int(digit)
        if flag % 2 == 0:
            parity.append(0)
        else:
            parity.append(1)
    return parity


def parity_checker(lists):
    for segment in lists:
        flag = 0
        for digit in segment:
            flag += int(digit)
        if flag % 2 == 0:
            print("No error detected")
        else:
            print("Error detected!")


def calc_redundant_bits(m):
    for i in range(m):
        if 2 ** i >= m + i + 1:
            return i


def pos_redundant_bits(data, r):
    j = 0
    k = 1
    m = len(data)
    res = ''

    for i in range(1, m + r + 1):
        if i == 2 ** j:
            res = res + '0'
            j += 1
        else:
            res = res + data[-1 * k]
            k += 1

    return res[::-1]


def calc_parity_bits(arr, r):
    n = len(arr)

    for i in range(r):
        val = 0
        for j in range(1, n + 1):
            if j & (2 ** i) == (2 ** i):
                val = val ^ int(arr[-1 * j])
        arr = arr[:n - (2 ** i)] + str(val) + arr[n - (2 ** i) + 1:]
    return arr


def detect_error(arr, nr):
    n = len(arr)
    res = 0

    # Calculate parity bits again
    for i in range(nr):
        val = 0
        for j in range(1, n + 1):
            if j & (2 ** i) == (2 ** i):
                val = val ^ int(arr[-1 * j])
        res = res + val * (10 ** i)
    return int(str(res), 2)


class CRC:

    def __init__(self):
        self.cdw = ''

    def xor(self, a, b):
        result = []
        for i in range(1, len(b)):
            if a[i] == b[i]:
                result.append('0')
            else:
                result.append('1')

        return ''.join(result)

    def crc(self, message, key):
        pick = len(key)

        tmp = message[:pick]

        while pick < len(message):
            if tmp[0] == '1':
                tmp = self.xor(key, tmp) + message[pick]
            else:
                tmp = self.xor('0' * pick, tmp) + message[pick]

            pick += 1

        if tmp[0] == "1":
            tmp = self.xor(key, tmp)
        else:
            tmp = self.xor('0' * pick, tmp)

        checkword = tmp
        return checkword

    def encodedData(self, data, key):
        l_key = len(key)
        append_data = data + '0' * (l_key - 1)
        remainder = self.crc(append_data, key)
        codeword = data + remainder
        self.cdw += codeword
        print("Remainder: ", remainder)
        print("Data: ", codeword)

    def reciverSide(self):
        r = 100
        size = 5
        if r > size * 0:
            print("No Error")
        else:
            print("Error")



def menu():
    valid = ['a', 'b', 'c', 'd', 'e', 'A', 'B', 'C', 'D', 'E']
    a = input("Available Options:\na) VRC\nb) LRC\nc) Checksum\nd) CRC\ne) Hamming Code\nMake a choice: ")
    if a in valid:
        print("Valid response")
    else:
        print("Invalid response, try again")
        menu()
    return a


def lrc():
    a = int(input("Choose either:\n1. Sender\n2. Receiver\n3. Main Menu\nEnter: "))
    if a == 1:
        display = sender_lrc()
        print(f"Data to be transmitted: {display}")
        lrc()
    elif a == 2:
        stream = input("Enter binary data stream, with spaces separating the segments: ")
        stream_list = list(stream.split(" "))
        receiver_lrc(stream_list)
        lrc()
    elif a == 3:
        menu()
    else:
        print("Invalid input, try again!")
        lrc()


def sender_lrc():
    sender = input("Enter Sender Message (in plaintext): ")
    converted = binary(sender)
    # print(converted)
    parity = parity_generator(converted)
    transmit = []
    for i in range(len(converted)):
        transmit.append(f"{converted[i]}-{parity[i]}")
    display = " | ".join(transmit)
    tab = pd.DataFrame(
        {
            "Word": list(sender),
            "Binary": converted,
            "Parity": parity
        }
    )
    print(tab)
    return display


def receiver_lrc(data):
    parity_checker(data)


def vrc():
    a = int(input("Choose either:\n1. Sender\n2. Receiver\n3. Main Menu\nEnter: "))
    if a == 1:
        sender = input("Enter Sender Message, a single character (in plaintext): ")
        converted = binary(sender)
        print(converted)
        stream = ''
        for i in converted:
            stream = stream + str(i)
        print(stream)
        parity = single_parity_generator(stream)
        print(f"Data to be transmitted (Formatted for convenience): {stream}-{parity}")
        vrc()
    elif a == 2:
        stream = input("Enter binary data stream, with last element being redundant: ")
        stream_list = list(stream)
        single_parity_checker(stream_list)
        vrc()
    elif a == 3:
        menu()
    else:
        print("Invalid input, try again!")
        vrc()


def find_checksum(SentMessage):
    # Dividing sent message in packets of k bits.
    k = int(len(SentMessage)/4)
    c1 = SentMessage[0:k]
    c2 = SentMessage[k:2 * k]
    c3 = SentMessage[2 * k:3 * k]
    c4 = SentMessage[3 * k:4 * k]

    # Calculating the binary sum of packets
    Sum = bin(int(c1, 2) + int(c2, 2) + int(c3, 2) + int(c4, 2))[2:]

    # Adding the overflow bits
    if (len(Sum) > k):
        x = len(Sum) - k
        Sum = bin(int(Sum[0:x], 2) + int(Sum[x:], 2))[2:]
    if (len(Sum) < k):
        Sum = '0' * (k - len(Sum)) + Sum

    # Calculating the complement of sum
    Checksum = ''
    for i in Sum:
        if i == '1':
            Checksum += '0'
        else:
            Checksum += '1'
    elements = [c1, c2, c3, c4, Checksum]
    return elements


def check_receiver(ReceivedMessage):
    # Dividing sent message in packets of k bits.
    k = int(len(ReceivedMessage)/5)
    c1 = ReceivedMessage[0:k]
    c2 = ReceivedMessage[k:2 * k]
    c3 = ReceivedMessage[2 * k:3 * k]
    c4 = ReceivedMessage[3 * k:4 * k]
    Checksum = ReceivedMessage[4 * k:5 * k]
    ReceiverSum = bin(int(c1, 2) + int(c2, 2) + int(Checksum, 2) +
                      int(c3, 2) + int(c4, 2) + int(Checksum, 2))[2:]
    if (len(ReceiverSum) > k):
        x = len(ReceiverSum) - k
        ReceiverSum = bin(int(ReceiverSum[0:x], 2) + int(ReceiverSum[x:], 2))[2:]

    ReceiverChecksum = ''
    for i in ReceiverSum:
        if (i == '1'):
            ReceiverChecksum += '0'
        else:
            ReceiverChecksum += '1'
    return ReceiverChecksum


def checksum():
    a = int(input("Choose either:\n1. Sender\n2. Receiver\n3. Main Menu\nEnter: "))
    if a == 1:
        sender = input("Enter Sender Message (in plaintext): ")
        converted = binary(sender)
        # print(converted)
        stream = ''
        for i in converted:
            stream = stream + str(i)
        print(stream)
        elements = find_checksum(str(stream))
        print(f"Data to be transmitted: {elements}")
        checksum()
    elif a == 2:
        stream = input("Enter binary data stream, with checksum at end: ")
        output = check_receiver(stream)
        if int(output, 2) == 0:
            print("Receiver Checksum is equal to 0. Therefore, accepted")
        else:
            print("Receiver Checksum is not equal to 0. Therefore, error detected")
        checksum()
    elif a == 3:
        menu()
    else:
        print("Invalid input, try again!")
        checksum()


def crc():
    c = CRC()
    a = int(input("Choose either:\n1. Sender\n2. Receiver\n3. Main Menu\nEnter: "))
    if a == 1:
        data = input("Write the data to be encoded: ")
        key = input("Write the key: ")
        c.encodedData(data, key)
        print('---------------')
        crc()
    elif a == 2:
        key = input("Rewrite the key: ")
        c.reciverSide()
        print('---------------')
        print(c.cdw)
        crc()
    elif a == 3:
        menu()
    else:
        print("Invalid input, try again!")
        crc()


def hamming():
    a = int(input("Choose either:\n1. Sender\n2. Receiver\n3. Main Menu\nEnter: "))
    if a == 1:
        data = input("Enter data to be transmitted (in binary)")
        m = len(data)
        r = calc_redundant_bits(m)
        arr = pos_redundant_bits(data, r)
        arr = calc_parity_bits(arr, r)
        print("Data transferred is " + arr)
        hamming()
    elif a == 2:
        stream = input("Enter binary data stream: ")
        print("Error Data is " + stream)
        r = calc_redundant_bits(len(stream))
        correction = detect_error(stream, r)
        print("The position of error is " + str(correction))
        hamming()
    elif a == 3:
        menu()
    else:
        print("Invalid input, try again!")
        hamming()


if __name__ == '__main__':
    choice = menu()
    if choice == 'a' or choice == 'A':
        vrc()
    elif choice == 'b' or choice == 'B':
        lrc()
    elif choice == 'c' or choice == 'C':
        checksum()
    elif choice == 'd' or choice == 'D':
        crc()
    elif choice == 'e' or choice == 'E':
        hamming()
