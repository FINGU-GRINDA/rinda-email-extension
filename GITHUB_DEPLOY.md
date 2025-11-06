# GitHub 배포 가이드

## 1단계: Git 사용자 정보 설정

터미널에서 다음 명령어를 실행하세요:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

또는 이 저장소에만 적용하려면:

```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## 2단계: 초기 커밋 생성

```bash
git commit -m "Initial commit: RINDA Email - AI-Powered Gmail Follow-up Assistant"
```

## 3단계: GitHub에서 새 저장소 생성

1. GitHub.com에 로그인
2. 우측 상단의 "+" 버튼 클릭 → "New repository" 선택
3. 저장소 정보 입력:
   - Repository name: `rinda-email` (또는 원하는 이름)
   - Description: "AI-Powered Gmail Follow-up Assistant"
   - Public 또는 Private 선택
   - **중요**: "Initialize this repository with a README" 체크하지 않기
4. "Create repository" 클릭

## 4단계: 원격 저장소 추가 및 푸시

GitHub에서 생성된 저장소의 URL을 복사한 후 (예: `https://github.com/yourusername/rinda-email.git`), 다음 명령어를 실행:

```bash
git remote add origin https://github.com/yourusername/rinda-email.git
git branch -M main
git push -u origin main
```

## 대안: GitHub CLI 사용 (설치된 경우)

GitHub CLI가 설치되어 있다면:

```bash
gh repo create rinda-email --public --source=. --remote=origin --push
```

## 확인

GitHub 저장소 페이지에서 모든 파일이 업로드되었는지 확인하세요.

