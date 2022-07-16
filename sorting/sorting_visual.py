import my_algorithms,time,os,sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
dimensions=(1024,512)
algorithms={"SelectionSort":my_algorithms.SelectionSort(),\
            "BubbleSort":my_algorithms.BubbleSort(),
            "MergeSort":my_algorithms.MergeSort(),
            "InsertionSort": my_algorithms.InsertionSort(),
            "RadixSort": my_algorithms.RadixSort(),
            "QuickSort":my_algorithms.QuickSort(),
            "HeapSort":my_algorithms.HeapSort()}
if len(sys.argv)>1:
    if sys.argv[1]=="list":
        for key in algorithms.keys():print(key,end=" ")
        print("")
        sys.exit(0)
pygame.init()
display=pygame.display.set_mode((dimensions[0],dimensions[1]))
display.fill(pygame.Color("white"))

def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
def update(algorithm,swap1=None,swap2=None,display=display):
    display.fill(pygame.Color("white"))
    pygame.display.set_caption("Sorting Visiualiser Algorithm: {} Time: {:.3f} Status: Sorting".format(algorithm.name, time.time() - algorithm.start_time))
    k=int(dimensions[0]/len(algorithm.array))
    for i in range(len(algorithm.array)):
        colour=(0,0,0)
        if swap1==algorithm.array[i]:
            colour=(0,255,0)
        elif swap2==algorithm.array[i]:
            colour=(255,0,0)
        pygame.draw.rect(display,colour,(i*k,dimensions[1],k,-algorithm.array[i]))
    check_events()
    pygame.display.update()
def keep_open(algorithm,display,time):
    pygame.display.set_caption("Sorting Visiualiser Algorithm: {} Time: {:.3f} Status: Done".format(algorithm.name, time))
    while True:
        check_events()
        pygame.display.update()
def main():
    if len(sys.argv)<2:
        print("Enter Choice")
    else:
        try:
            algorithm = algorithms[sys.argv[1]]
            try:
                time_elapsed=algorithm.run()[1]
                keep_open(algorithm,display,time_elapsed)
            except:
                pass
        except:
            print("Error: {} is not a valid sorting algorithm".format(sys.argv[1]))
if __name__=="__main__":
    main()
