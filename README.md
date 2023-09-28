

<div align=center><img src="https://capsule-render.vercel.app/api?type=rounded&color=auto&height=150&section=header&text=MOOCHU&fontSize=90" /></div>

## MOOCHU PROJECT

    `MOOCHU` 는 OTT, 영화관의 영화들의 데이터들을 한 곳에서
    저장된 영화를 기반으로 사용자마다 좋아하는 영화, TV show를 추천 받을 수 있는
    `영화 추천 시스템 웹 서비스` 입니다.

<br>

<details>
<summary>🎤 MOOCHU 바로가기</summary>
<div markdown="1">

<br>
<a href="http://34.64.147.118:8000/moochu" target="_blank" rel="noopener noreferrer">👉🏻Click👈🏻</a>
<br>
</div>
</details>

<br>

## 🧑‍🤝‍🧑 제작 기간 & 참여 인원

  	-  제작 기간 : 2023.06.12 ~ 2023.08.11 (약 2개월)
	-  참여 인원 : 6명
<br>

## ⚙️ 사용 기술 스택

<br>

| ⚙️ 기술 스택 | 👇🏻 사용 목적 |
|--|--|
| **`django`** | MOOCHU 웹 서비스 구현 |
| **`airflow`** | CGV, Lotte, MegaBox, OTT 개봉예정작 데이터 자동화|
| **`docker`**, **`docker compose`** | 배포를 위한 작업 환경 도커라이징 |
| **`GCP(Google Cloud Platform)`** | 배포를 위한 클라우드 서비스 활용 |
| **`Google Cloud Storage`** | Data Warehouse, 이미지 적재 |
| **`Mysql`**, **`mongoDB`** | 데이터베이스 활용 |
| **`nginx`**, **`gunicorn`** | Web서버와 WAS 분리 |
| **`fastapi`** | 추천 모델 serving |
| **`Google BigQuery`** | Data Warehouse, 학습된 모델 파일 적재 |
| **`Kafka`** , **`redis`** | 트래픽 분산, 로그 적재 |
| **`elastic search`**, **`logstash`**, **`kibana`** | 검색 기능 고도화, 데이터 시각화 |

<br>

## ERD 설계
	
![DB ERD](https://github.com/jsjang96/images/blob/master/MOOCHU_erd.png)

<br>

## 핵심 기능
- 이 서비스의 핵심 기능은 **추천 서비스 기능**입니다. <br>
- 사용자가 즐겨서 보는 영화 장르, 영화 리스트를 기반으로 새로운 영화를 추천해주는 서비스입니다. <br>
- 또한, 영화들을 사용자들끼리 추천을 해주고 미니홈피를 만들어 소통도 할 수 있도록 했습니다. <br>
- 그리고, 장르와 OTT별로 본인이 좋아하는 영화들을 필터링하여 볼 수 있습니다.<br>
아래는 **전체 아키텍처**에 대한 첨부파일입니다.

<details>
<summary><b>전체 아키텍처 펼치기</b></summary>
<div align="center" markdown="1">
	<img src="https://github.com/jsjang96/images/blob/master/%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%981.png"/>
	<img src="https://github.com/jsjang96/images/blob/master/%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%982.png"/>
	<img
src="https://github.com/jsjang96/images/blob/master/%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%983.png"/>
</div>
</details>
<br>

## 담당역할
<br>

### 1. 영화, TV show 대량 데이터 수집 및 전처리
<br>

- 영화 정보 제공 api인 TMDB API를 활용하여 파이썬 코드를 기간별로 구분지어 영화 정보를 약 60만건 수집하였습니다.

- 하지만 팀원들이 원하는 데이터가 없었기 때문에 논의를 통해 해당 데이터를 포기하게 되었습니다.

<br>

- 셀레니움을 이용하여 netflix 사이트를 직접 크롤링하는 작업, "키노라이츠"라는 사이트에서도 데이터들을 모았습니다.

- 각각의 사이트에서 세부정보를 가져오는 과정에서 과도한 트래픽으로 IP Blocking을 당하여 전체 데이터를 가져오는데 문제가 있었습니다.
 
- 영화 고유 id값들을 6분할을 해서 팀원들이 각자의 ip에서 크롤링을 하였습니다.
 	- json파일로 저장하여 병합하고 전처리를 하였습니다.
  
**알게된 점**
- 꽤 많은 시간이 걸려 진행한 프로세스일지라도 서로의 의견을 조율하여 빠르게 방안을 찾아가는 것이 중요하다는 것을 느꼈습니다.
  
- 데이터를 수집(크롤링)하는 과정에서 가져올 수 있는 정보들은 다 가져온 후 data lake에 적재 ->
          이후 전처리하여 datawharehouse를 구축하면 더 효율적인 일처리가 가능하다는 것을 알게 되었습니다.
    
- 프로젝트를 하며 전처리를 할때 각 파트별로 필요한 부분을 확실히 설정해놓으면 시간을 절약할 수 있었습니다.
    
- jira와 confluence 를 이용하여 일정 및 상황을 공유하면 팀원에게 따로 요청을 하지 않더라도 서로 필요한 부분을 공유할 수 있었습니다.

<br>

### 2. Airflow를 통한 자동화 
Airflow repository : <a href="https://github.com/w00dy2/moochu_airflow">
  <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</a>

<br>   	

  ### 2.1 크롤링 덱 자동화
  
  - 팀원들과 함께 각자 작성해놓은 크롤링 코드를 통합하는 작업과, 이를 Airflow dag으로 만드는 작업을 하였습니다.
  
  - 팀원들과 어떠한 방법과 기준으로 크롤링 코드를 짰는지에 대해 코드리뷰를 하였고,<br>
    통합방안에 대해 고민하고 코드를 개선할 수 있었습니다.
  
  **Work Flow**
  
    - Airflow를 통해 MEGABOX, CGV, DAUM영화 에서 순차적으로 데이터를 수집 -> 
    
    - 중복 값은 제거하며, OTT 컬럼에 해당되는 페이지를 추가 ->
    
    - mongodb에 데이터를 적재 ->
    
    - mongodb에서 자동으로 생성된 고유한 정보인 _id필드를 기준으로 poster image의 이름을 설정->
    
    - Google Cloud Storage에 적재하는 과정을 daily 배치로 airflow 자동화를 하였습니다.

    
  ### 2.2 사용자기반 추천 모델 자동화
   - big Query ML으로 추천모델을 구상했지만 여건상 jupyter로 모델을 실행하게 되었습니다.
     
  **Work Flow**
    
    - django에서 Bigquery에 적재한 사용자의 로그데이터를 분석 ->
    
    - 사용자의 예상평점을 분석 및 추천 미디어 100개를 산출 ->
    
    - Redis로 전송하여 사용자에게 추천하는 모델
    
    - Airflow로 추천모델을 구축해놓은 컨테이너로 ssh 연결
    
    - 하루에 한번 추천 모델을 실행 (사용자가 적은 시간대인 AM 3:00)
    
    - 실행 결과 slack api를 이용하여 확인  

    


### 3. mongoDB에 데이터 적재, mongoDB와 django연동
  <br>
	  
- 영화 데이터 중 줄거리등의 컬럼에서 비정형 데이터가 생기는 경우가 있었습니다.
- 이를 json 형식으로 저장하여 일어날 수 있는 이슈를 최소화 하고자 mongoDB를 사용했습니다.

- 서비스용 DB를 구축하기 이전 K-ICT에서 무료로 할당받은 개발 서버를 이용하여 mongoDB를 구축하고 테스트용 DB로 이용할 수 있었습니다.
- pymongo를 통해 django와 연동을 하는 과정에서 발생하는 이슈를 미리 모니터링 할 수 있었습니다.

- 모니터링 과정에서는 OTT별로 collection을 나눠주고 분류했으며,
- 실제 서비스용 DB를 구축함에 있어서는 OTT key를 따로 만들어 병합하는 과정을 거쳤으며,
- 이를 통해 중복 영화 정보를 제거, 약 10만건 -> 4만건 으로 DB를 슬림하게 만들었습니다.

### 4. django
#### 4.1 django 개봉예정작 페이지 제작
    
  - 영화 및 TV 프로그램의 개봉예정작 페이지를 제작하였습니다.
  - mongoDB에 있는 데이터들을 django에 가져와서 view단에서 today를 기준으로 공개예정일을 계산하여 페이지로 구현하였습니다.
  - 각각의 영화 데이터가 어디에서 볼 수 있는지도 포스터 우측상단에서 보여줄 수 있게 작업하였습니다.
 
  - 

#### 4.2 pagenation 코드 수정

- db 구축 및 page 작업을 같이하던 팀원의 필터링 기능에서 필터를 해제하고 검색할 경우 data가 뜨지 않는 문제가 발생
  -> 해당 views에 조건문을 추가하여 설정해놓은 id값에 아무것도 추가되지 않았을경우 첫 페이지로 return되게 설정
  
**알게된 점**

- 처음에는 mongoDB의 데이터를 django와 mongodb가 연동이 가능한 djongo를 이용하라는 글이 많아서 해당 방법을 시도하였지만,
  mongodb에 update, delete 작업이 아닌 data를 read 작업만 필요하였기에 pymongo로도 충분히 구현이 가능하다는 것을 알 수 있었습니다.




## 트러블 슈팅

### 1. DB 적재
1.1 tmdb api 활용하여 데이터를 수집
- 매일 신규 데이터를 자동으로 추가하는 airflow dag까지 완성해놓은 상태였지만 팀원들과 상의 끝에 해당데이터를 사용하지 않기로 함. <br>
  

1.2 셀레니움을 이용하여 직접 OTT 사이트를 크롤링할 경우 지속적인 서비스 유지에 있어 airflow 배치가 불가능하다는 문제가 발생
- 방안 : 데이터를 가져오는 방식을 requeests로 수정하였습니다.<br>

1.3 크롤링을 통해 메인 db를 구축하는 과정에 있어서 일정 데이터 개수가 넘어가면 IP blocking이 발생
- 방안 : 팀원들에게 부탁하여 각자 다른장소에서 일정량의 데이터를 수집할 수 있었습니다.
<br>


<br>

### 2. Airflow - mongodb - googlestorage

2.1 각각의 덱을 짜서 작업을 실행했을경우 같은 영화 정보를 처리하기 위해 read write를 계속 반복해야하는 문제가 있었습니다.<br>
- 하나의 덱으로 만들어 중복 데이터를 처리할 수 있게 작성하였습니다.<br>

2.2 직접 서비스를 최대한 구현하는 것을 목표로 하며 포스터 이미지를 직접 storage에 적재하여 보여주는 방식으로 변경하게되었습니다.<br>
- 이미지들의 고유한 id를 이용하기 위해 mongodb에서 자동 생성한 고유필드인 _id를 기준으로 storage에 적재하기로 결정하였습니다.<br>
<br>
2.2.1 이미 저장된 데이터에서 이미지를 적재하는 것은 문제가 되지 않았지만,
	마감일까지 시간이 얼마 남지 않은 상황에서 airflow dag에 이미지적재를 추가하는 것은 부담감이 컸습니다.<br>
<br>
- 필요한 데이터가 무엇인지에 대해 생각을 하며 최대한 효율적인 airflow dag의 관점에서만 생각하려고 노력하였습니다.<br>
<br>
  2.2.2 이미지를 적재하는 과정에서 DB를 조회하게 되면 그만큼 시간과 리소스 사용이 많아지기 때문에 이를 줄일 필요가 있었습니다.<br>
<br>
   -> xcom을 이용하여 mongodb에 적재되는 과정에서 알 수 있는 _id값과 href 값을 넘겨주기로 결정 (limit 48kb) <br>
   - 각각의 task에서 push한 xcom을 merge하는 task를 거쳐 googlestorage 적재 task를 실행하여 불필요한 리소스 사용을 줄일 수 있었습니다.<br>


  <br>
</div>
