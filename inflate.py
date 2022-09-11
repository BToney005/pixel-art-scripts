import os, sys, time
from PIL import Image

def find_arg(flag: str) -> any:
    try:
        i = sys.argv.index(flag)
        return sys.argv[i+1]
    except:
        return None

def inflate(file_in: str, file_out: str, multiply_by: int) -> None:

    try:
        img_in = Image.open(file_in, 'r')
        width, height = img_in.size
        pix_values = list(img_in.getdata()) 

        out_width = width * multiply_by
        out_height = height * multiply_by

        img_bytes = []

        pix_map = []

        row = []
        for v in pix_values:
            if len(row) < width:
                row.append(v)
            else:
                pix_map.append(row)
                row = [v]
        pix_map.append(row)

        for nx in range(0,out_width):
            for ny in range(0, out_height):

                x = int(nx / multiply_by)
                y = int(ny / multiply_by)

                pix = pix_map[x][y]

                img_bytes.append(pix[0])
                img_bytes.append(pix[1])
                img_bytes.append(pix[2])

        img_in.close()


        img_out = Image.frombytes('RGB', (out_width, out_height), bytes(img_bytes))
        img_out.save(file_out)

    except: 
        print ('Error converting file.')

if __name__ == '__main__':
    src_file = None 
    dest_file = None
    multiplier = 4

    src_file = find_arg('-in')
    dest_file = find_arg('-out')
    multiplier = find_arg('-m')

    if src_file is None:
        raise Exception('No input file provided.')
    if src_file[-4:] != '.png':
        raise Exception('Input file must be a png.')
    if not os.path.exists(src_file):
        raise Exception('The given input file does not exist.')

    if multiplier is None:
        multiplier = 4
    else:
        multiplier = int(multiplier)

    if dest_file is None:
        head, tail = os.path.split(src_file)        
        name = tail[:-4]
        epoch = time.asctime( time.gmtime(0) )
        curr_time = round(time.time()*1e3) 
        dest_file = '%s/%s_x_%d_%d.png'  % ( head, name, multiplier, curr_time)

    if os.path.isdir(dest_file):
        name = os.path.basename(src_file)[:-4]
        epoch = time.asctime( time.gmtime(0) )
        curr_time = round(time.time()*1e3) 
        dest_file = '%s/%s_inflated_x_%d_%d.png'  % ( dest_file[:-1] if dest_file[-1] == '/' else dest_file, name, multiplier, curr_time)
        pass
    else:
        if src_file[-4:] != '.png':
            raise Exception('Output file must be a png.')
        if not os.path.exists(dest_file):
            head, tail = os.path.split(src_file)        
            if not os.path.isdir(head):
                raise Exception('The given output file does not exist.')

    inflate(src_file, dest_file, multiplier)