# generate_ChalkBoards
Generating training data for [ChalkMail](https://github.com/innovationgarage/ChalkMail/)

## How to use:
- clone this repository
- download [quickdraw](https://github.com/googlecreativelab/quickdraw-dataset) data:

        # from generate_ChalkBoards/src/
        ./get_data.sh

- generate boards (checkout all the arguments in main.py)

        # from generate_ChalkBoards/src/
        python main.py --seed 42 --no_boards 10 --no_drawings 100
        

- generated boards will be saved in __generate_ChalkBoards/boards/__
- bounding boxes for each board is available in __generate_ChalkBoards/labels/__
- collective labels is availabe in __generate_ChalkBoards/labels/all_labels.csv__
