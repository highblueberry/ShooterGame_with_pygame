# shooting_game with pygame
'strikers 1945'라는 과거 많은 오락실을 점령했던 비행기 슈팅 게임을 오마쥬하여 클래식한 슈팅게임을 만들었습니다.<br/>
<br/><br/>

## 특징
기본적인 슈팅게임처럼 탄막 피하기 위주의 게임을 만들고자 했고, 특수패턴이 있는 보스가 있습니다.

<br/><br/>


## 준비물
2가지 모듈이 필요합니다. 
```
pip install pygame
pip install random
```
또한 게임에 사용되는 이미지를 다운받아야 합니다.
<br/> 
![health](https://github.com/highblueberry/ShooterGame_with_pygame/assets/59508874/18579cdd-ab59-4a2f-927a-adc469c6e7af)
![missile](https://github.com/highblueberry/ShooterGame_with_pygame/assets/59508874/71cdc4c6-901a-460b-b2e1-f18612625a19)
![heal_potion](https://github.com/highblueberry/ShooterGame_with_pygame/assets/59508874/33f37fc7-b05e-44da-b335-90d5a32a32b9)


<br/><br/>

## 게임설명
* 적군 기체와 적군의 탄막을 피하며 일정 수 이상의 
적군을 잡으면 보스가 출현합니다. <br/>

* 보스를 잡으면 "Game Over"와 점수합산과 함께 게임이 종료됩니다. <br/>

* 보스를 잡기 전에 주어지는 5개의 체력을 모두 잃으면 마찬가지로 "Game Over"와 점수합산 함께 게임이 종료됩니다.
<br/><br/>
![game_over](https://github.com/highblueberry/ShooterGame_with_pygame/assets/59508874/be8067be-d9fd-4351-bbc6-73d2c83c919b)
![game_win](https://github.com/highblueberry/ShooterGame_with_pygame/assets/59508874/34107a52-aa0b-4d0b-95b4-d089d32c4e96)



<br/><br/> 
* 방향키로 이동하고 'z'키로 공격을 할 수 있습니다. <br/>
* 적군을 격추시 일정 확률로 물약을 드랍하고 2가지 기능이 있습니다.
    1. 플레이어의 체력 회복
    2. 플레이어 체력이 모두 차있을 때 플레이어 공격 강화
 ![물약](https://github.com/highblueberry/ShooterGame_with_pygame/assets/59508874/19ac422e-a5a4-4d76-bf06-0a125c6079ed)

  

* 공격은 발사수가 2개, 3개 순으로 강화됩니다. <br/>
![공격1](https://github.com/highblueberry/ShooterGame_with_pygame/assets/59508874/2bdd7db1-9aa6-4eac-b253-f9c8584acb63)
![공격2](https://github.com/highblueberry/ShooterGame_with_pygame/assets/59508874/1034170b-138d-4be6-980a-915d0373bfe7)
![공격3](https://github.com/highblueberry/ShooterGame_with_pygame/assets/59508874/9dc1e438-9012-4061-b49e-4ee5b040af04)




<br/> 적군의 종류는 3종류입니다.
* 일반기
* 대장기
* 보스
<br/>
일반기와 대장기는 공격 패턴이 동일하지만 체력에서 차이가납니다.
![일반기](https://github.com/highblueberry/ShooterGame_with_pygame/assets/59508874/e904dfd7-7b11-4f3d-b5e3-65b88481784a)
![대장기](https://github.com/highblueberry/ShooterGame_with_pygame/assets/59508874/5414a678-7e0a-4a01-bbfa-c00aa760b63b)
![보스](https://github.com/highblueberry/ShooterGame_with_pygame/assets/59508874/0cc8e90c-8056-4e58-b613-c5f8d640638e)
<br/><br/>

적군을 20기 이상 격추시키면 보스가 등장합니다.<br/>
보스는 일자로 탄을 발사하는 특수패턴으로 이루어져 있습니다. <br/>
일자 탄이 어디로 날라올지는 확률이 동일한 랜덤으로 정해집니다.<br/>
![화면3](https://github.com/highblueberry/ShooterGame_with_pygame/assets/59508874/c32fe600-7348-4f6d-82fd-d5262529a369)




## 아쉬운점
충돌 알고리즘을 직접 개발한 것이 아니라서 히트박스 판정이 본래 이미지보다 넓습니다. 다음과 같은 방법으로 개선이 가능합니다. <br/><br/>
* 플레이어 기체 사진을 분해하여 사용하기
* 히트박스를 플레이어 기체가 아닌 다른 것으로 지정해주기


## developer
* 20101266 이동은

## reference
* https://www.youtube.com/watch?v=reLCH8TWQJ8&t=538s - 기체 충돌부분 구현 참고
* https://www.youtube.com/watch?v=sHu7UBumW8I&t=338s - game over와 game win의 경우 텍스트 출력 방법 참고
