names="circle  envelope  hexagon  line  octagon  square  triangle  zigzag"
for name in $names
do
mkdir "../data/"    
wget -O "../data/"$name".npy" "https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/"$name".npy"
done
echo "All done!"
