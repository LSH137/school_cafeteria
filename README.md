# school_cafeteria

이 프로그램을 실행시키기 위해서는 numpy, matplotlib가 필요합니다
파이참에서 이 폴더를 연 뒤에 main.py를 실행시키면 한 번에 급식을 먹으러 오는 학생 수를 설정할 수 있습니다

main.py:
한 번에 급식을 먹으러 오는 학생 수를 설정하고 정규분포에 따라 친구의 수와 밥 먹는데 걸리는 시간을 정한다.

스케줄링을 한다. 스케줄링은 scheduling.py에 정의되어있는 함수를 통해 구현되어 있다.

학생들이 병렬적으로 밥을 먹는 것을 구현하기 위해 학생 1명당 스레드 1개를 할당하여 밥을 먹도록 한다.

남은 자리 수를 저장하기 위한 스레드도 하나 생성하여 모든 학생들이 밥을 다 먹을 때까지 실행되면서 시간에 따라 남은 자리 수를 기록한다

matplotlib를 이용하여 그래프를 그린다


scheduling.py

SJF: Shortest Job First
급식실에 들어오기 전에 줄을 서 있는 학생 중 앞쪽 10명의 학생 중 5명 이하의 일행인 학생을 먼저 급식실로 입장시키고, 5명 이상인 학생들을 그 다음으로 입장시킨다. 

LJF: Longest Job First
급식실에 들어오기 전에 줄을 서 있는 학생 중 앞쪽 10명의 학생 중 5명 이상의 일행인 학생을 먼저 급식실로 입장시키고, 5명 이하인 학생들을 그 다음으로 입장시킨다. 

FCFS: First Come First Serve
선착순으로 급식실에 입장시킨다

func.py
여럿이서 같이 밥을 먹는 경우와 혼자 밥을 먹는 경우에 대해 프로그래밍 되어 있다.
여럿이서 밥을 같이 먹는 경우, 일행이 같이 앚을 연속된 자리를 찾지 못하면 5초 후에 다시 탐색하고 그래도 자리가 없으면 각자 알아서 먹는다

DataStructure.py
학생들과 급식실 배식구가 클래스로 구현되어 있다.
