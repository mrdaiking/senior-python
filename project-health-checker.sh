#!/bin/bash

# 🏥 Universal Project Health Checker
# Usage: ./project-health-checker.sh [project-path]
# Author: Senior Developer Assistant

set -e

PROJECT_PATH=${1:-.}
cd "$PROJECT_PATH"

echo "🏥 ==============================================="
echo "   UNIVERSAL PROJECT HEALTH CHECKER"
echo "   Project: $(basename $(pwd))"
echo "   Path: $(pwd)"
echo "   Date: $(date)"
echo "==============================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Score tracking
TOTAL_CHECKS=0
PASSED_CHECKS=0

check_status() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC} - $2"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        echo -e "${RED}❌ FAIL${NC} - $2"
        if [ -n "$3" ]; then
            echo -e "${YELLOW}   💡 Suggestion: $3${NC}"
        fi
    fi
}

warn_status() {
    echo -e "${YELLOW}⚠️  WARN${NC} - $1"
    if [ -n "$2" ]; then
        echo -e "${YELLOW}   💡 Suggestion: $2${NC}"
    fi
}

info_status() {
    echo -e "${BLUE}ℹ️  INFO${NC} - $1"
}

echo ""
echo "🔍 DETECTING PROJECT TYPE..."

# Detect project type
PROJECT_TYPE="unknown"
if [ -f "package.json" ]; then
    PROJECT_TYPE="nodejs"
    info_status "Node.js/JavaScript project detected"
elif [ -f "pom.xml" ] || [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then
    PROJECT_TYPE="java"
    info_status "Java project detected"
elif [ -f "*.csproj" ] || [ -f "*.sln" ] || [ -f "global.json" ]; then
    PROJECT_TYPE="dotnet"
    info_status ".NET project detected"
elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ] || [ -f "setup.py" ]; then
    PROJECT_TYPE="python"
    info_status "Python project detected"
elif [ -f "Cargo.toml" ]; then
    PROJECT_TYPE="rust"
    info_status "Rust project detected"
elif [ -f "go.mod" ]; then
    PROJECT_TYPE="go"
    info_status "Go project detected"
elif [ -f "pubspec.yaml" ]; then
    PROJECT_TYPE="flutter"
    info_status "Flutter project detected"
elif [ -f "android/build.gradle" ] || [ -f "app/build.gradle" ]; then
    PROJECT_TYPE="android"
    info_status "Android project detected"
fi

echo ""
echo "🏗️  PROJECT STRUCTURE CHECKS"
echo "----------------------------------------"

# 1. Version Control
if [ -d ".git" ]; then
    check_status 0 "Git repository initialized"
    
    # Check if there are commits
    if git rev-parse HEAD >/dev/null 2>&1; then
        check_status 0 "Git has commits"
        
        # Check for uncommitted changes
        if [ -z "$(git status --porcelain)" ]; then
            check_status 0 "No uncommitted changes"
        else
            warn_status "Uncommitted changes detected" "Commit or stash your changes"
        fi
    else
        warn_status "No commits found" "Make your first commit"
    fi
else
    check_status 1 "Git repository" "Run: git init"
fi

# 2. README
if [ -f "README.md" ] || [ -f "README.rst" ] || [ -f "README.txt" ]; then
    check_status 0 "README file exists"
else
    check_status 1 "README file" "Create README.md with project description"
fi

# 3. License
if [ -f "LICENSE" ] || [ -f "LICENSE.md" ] || [ -f "LICENSE.txt" ]; then
    check_status 0 "License file exists"
else
    warn_status "No license file found" "Add LICENSE file for open source projects"
fi

# 4. .gitignore
if [ -f ".gitignore" ]; then
    check_status 0 ".gitignore exists"
else
    check_status 1 ".gitignore file" "Create .gitignore to exclude build artifacts"
fi

echo ""
echo "🤖 CI/CD CHECKS"
echo "----------------------------------------"

# 5. CI/CD Configuration
CI_FOUND=0
if [ -d ".github/workflows" ] && [ "$(ls -A .github/workflows 2>/dev/null)" ]; then
    check_status 0 "GitHub Actions workflows found"
    CI_FOUND=1
elif [ -f ".gitlab-ci.yml" ]; then
    check_status 0 "GitLab CI configuration found"
    CI_FOUND=1
elif [ -f "Jenkinsfile" ]; then
    check_status 0 "Jenkins pipeline found"
    CI_FOUND=1
elif [ -f ".travis.yml" ]; then
    check_status 0 "Travis CI configuration found"
    CI_FOUND=1
elif [ -f "azure-pipelines.yml" ]; then
    check_status 0 "Azure Pipelines configuration found"
    CI_FOUND=1
fi

if [ $CI_FOUND -eq 0 ]; then
    check_status 1 "CI/CD configuration" "Set up GitHub Actions, GitLab CI, or other CI/CD"
fi

echo ""
echo "🧪 TESTING SETUP"
echo "----------------------------------------"

# 6. Testing (project-specific)
case $PROJECT_TYPE in
    "nodejs")
        if grep -q "\"test\":" package.json 2>/dev/null; then
            check_status 0 "Test script configured in package.json"
        else
            check_status 1 "Test script in package.json" "Add test script"
        fi
        
        if [ -d "test" ] || [ -d "tests" ] || [ -d "__tests__" ] || [ -d "spec" ]; then
            check_status 0 "Test directory exists"
        else
            check_status 1 "Test directory" "Create test directory and add tests"
        fi
        ;;
        
    "python")
        if [ -f "pytest.ini" ] || [ -f "pyproject.toml" ] || [ -f "setup.cfg" ]; then
            check_status 0 "Test configuration found"
        else
            warn_status "No test configuration found" "Configure pytest or unittest"
        fi
        
        if [ -d "tests" ] || [ -d "test" ]; then
            check_status 0 "Test directory exists"
        else
            check_status 1 "Test directory" "Create tests/ directory"
        fi
        ;;
        
    "java")
        if [ -d "src/test" ]; then
            check_status 0 "Test directory exists (src/test)"
        else
            check_status 1 "Test directory" "Create src/test/java directory"
        fi
        ;;
        
    "dotnet")
        if find . -name "*.Tests.csproj" -o -name "*Test*.csproj" | grep -q .; then
            check_status 0 "Test project found"
        else
            check_status 1 "Test project" "Create test project with dotnet new xunit"
        fi
        ;;
        
    *)
        if [ -d "test" ] || [ -d "tests" ]; then
            check_status 0 "Test directory exists"
        else
            warn_status "No test directory found" "Create tests directory"
        fi
        ;;
esac

echo ""
echo "📊 CODE QUALITY TOOLS"
echo "----------------------------------------"

# 7. Linting and formatting (project-specific)
case $PROJECT_TYPE in
    "nodejs")
        if [ -f ".eslintrc.js" ] || [ -f ".eslintrc.json" ] || [ -f ".eslintrc.yml" ]; then
            check_status 0 "ESLint configuration found"
        else
            check_status 1 "ESLint configuration" "Add .eslintrc.json"
        fi
        
        if [ -f ".prettierrc" ] || [ -f ".prettierrc.json" ] || [ -f "prettier.config.js" ]; then
            check_status 0 "Prettier configuration found"
        else
            warn_status "No Prettier configuration" "Add .prettierrc for code formatting"
        fi
        ;;
        
    "python")
        if [ -f "pyproject.toml" ]; then
            if grep -q "black\|flake8\|isort\|mypy" pyproject.toml 2>/dev/null; then
                check_status 0 "Code quality tools configured in pyproject.toml"
            else
                warn_status "No linting tools in pyproject.toml" "Add black, flake8, isort, mypy"
            fi
        else
            warn_status "No pyproject.toml found" "Create pyproject.toml with tool configurations"
        fi
        ;;
        
    "java")
        if [ -f "checkstyle.xml" ] || grep -q "checkstyle\|spotbugs\|pmd" pom.xml build.gradle 2>/dev/null; then
            check_status 0 "Code quality tools configured"
        else
            warn_status "No code quality tools found" "Add CheckStyle, SpotBugs, or PMD"
        fi
        ;;
        
    "dotnet")
        if [ -f ".editorconfig" ]; then
            check_status 0 "EditorConfig found"
        else
            warn_status "No .editorconfig found" "Add .editorconfig for consistent formatting"
        fi
        ;;
esac

echo ""
echo "🐳 CONTAINERIZATION"
echo "----------------------------------------"

# 8. Docker
if [ -f "Dockerfile" ]; then
    check_status 0 "Dockerfile exists"
    
    # Check for multi-stage build
    if grep -q "FROM.*AS" Dockerfile 2>/dev/null; then
        check_status 0 "Multi-stage Docker build detected"
    else
        warn_status "Single-stage Docker build" "Consider multi-stage build for smaller images"
    fi
    
    # Check for non-root user
    if grep -q "USER\|useradd\|adduser" Dockerfile 2>/dev/null; then
        check_status 0 "Non-root user configured in Docker"
    else
        warn_status "Running as root in Docker" "Add non-root user for security"
    fi
else
    warn_status "No Dockerfile found" "Create Dockerfile for containerization"
fi

# 9. Docker Compose
if [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ]; then
    check_status 0 "Docker Compose configuration exists"
    
    # Check for health checks
    if grep -q "healthcheck" docker-compose.y*ml 2>/dev/null; then
        check_status 0 "Health checks configured in Docker Compose"
    else
        warn_status "No health checks in Docker Compose" "Add healthcheck configurations"
    fi
else
    warn_status "No Docker Compose found" "Create docker-compose.yml for multi-service setup"
fi

echo ""
echo "🔒 SECURITY CHECKS"
echo "----------------------------------------"

# 10. Dependencies security
case $PROJECT_TYPE in
    "nodejs")
        if command -v npm >/dev/null 2>&1; then
            if npm audit --audit-level=high >/dev/null 2>&1; then
                check_status 0 "No high-severity npm vulnerabilities"
            else
                check_status 1 "NPM security audit" "Run: npm audit fix"
            fi
        fi
        ;;
        
    "python")
        if command -v safety >/dev/null 2>&1; then
            if safety check >/dev/null 2>&1; then
                check_status 0 "No known Python vulnerabilities (safety)"
            else
                warn_status "Python vulnerabilities detected" "Run: safety check --full-report"
            fi
        else
            warn_status "Safety not installed" "Install: pip install safety"
        fi
        ;;
esac

# 11. Secrets detection
if [ -f ".env" ] && ! grep -q ".env" .gitignore 2>/dev/null; then
    check_status 1 ".env file not in .gitignore" "Add .env to .gitignore"
else
    check_status 0 "No .env file committed"
fi

# Check for common secrets patterns
if grep -r -i "password\|secret\|key\|token" --include="*.js" --include="*.py" --include="*.java" --include="*.cs" . 2>/dev/null | grep -v node_modules | grep -v ".git" | head -1 >/dev/null; then
    warn_status "Potential secrets in code" "Review hardcoded credentials and use environment variables"
fi

echo ""
echo "📈 MONITORING & LOGGING"
echo "----------------------------------------"

# 12. Logging configuration
LOGGING_FOUND=0
case $PROJECT_TYPE in
    "nodejs")
        if grep -q "winston\|bunyan\|pino" package.json 2>/dev/null; then
            check_status 0 "Logging library found in package.json"
            LOGGING_FOUND=1
        fi
        ;;
        
    "python")
        if grep -q "loguru\|structlog" pyproject.toml requirements.txt 2>/dev/null; then
            check_status 0 "Advanced logging library found"
            LOGGING_FOUND=1
        fi
        ;;
        
    "java")
        if grep -q "logback\|slf4j\|log4j" pom.xml build.gradle 2>/dev/null; then
            check_status 0 "Logging framework found"
            LOGGING_FOUND=1
        fi
        ;;
esac

if [ $LOGGING_FOUND -eq 0 ]; then
    warn_status "No advanced logging library detected" "Consider structured logging libraries"
fi

# 13. Health check endpoint
if grep -r -i "health\|ping\|status" --include="*.js" --include="*.py" --include="*.java" --include="*.cs" . 2>/dev/null | grep -v node_modules | grep -v ".git" | head -1 >/dev/null; then
    check_status 0 "Health check endpoint likely implemented"
else
    warn_status "No health check endpoint found" "Add /health or /ping endpoint"
fi

echo ""
echo "📚 DOCUMENTATION"
echo "----------------------------------------"

# 14. API Documentation
if [ -f "swagger.json" ] || [ -f "openapi.json" ] || [ -f "swagger.yml" ] || [ -f "openapi.yml" ]; then
    check_status 0 "API documentation (OpenAPI/Swagger) found"
elif grep -r -i "swagger\|openapi" --include="*.js" --include="*.py" --include="*.java" --include="*.cs" . 2>/dev/null | head -1 >/dev/null; then
    check_status 0 "API documentation framework detected in code"
else
    warn_status "No API documentation found" "Add OpenAPI/Swagger documentation"
fi

# 15. Code documentation
case $PROJECT_TYPE in
    "python")
        if find . -name "*.py" -exec grep -l "\"\"\"" {} \; | head -1 >/dev/null 2>&1; then
            check_status 0 "Python docstrings found"
        else
            warn_status "No Python docstrings detected" "Add docstrings to functions and classes"
        fi
        ;;
        
    "java")
        if find . -name "*.java" -exec grep -l "/\*\*" {} \; | head -1 >/dev/null 2>&1; then
            check_status 0 "Javadoc comments found"
        else
            warn_status "No Javadoc comments detected" "Add Javadoc to public methods"
        fi
        ;;
        
    "nodejs")
        if find . -name "*.js" -exec grep -l "/\*\*" {} \; | head -1 >/dev/null 2>&1; then
            check_status 0 "JSDoc comments found"
        else
            warn_status "No JSDoc comments detected" "Add JSDoc documentation"
        fi
        ;;
esac

echo ""
echo "⚡ PERFORMANCE & SCALABILITY"
echo "----------------------------------------"

# 16. Dependency management
case $PROJECT_TYPE in
    "nodejs")
        if [ -f "package-lock.json" ] || [ -f "yarn.lock" ]; then
            check_status 0 "Dependency lock file exists"
        else
            check_status 1 "Dependency lock file" "Commit package-lock.json or yarn.lock"
        fi
        ;;
        
    "python")
        if [ -f "poetry.lock" ] || [ -f "Pipfile.lock" ]; then
            check_status 0 "Python dependency lock file exists"
        else
            warn_status "No Python lock file" "Use Poetry or Pipenv for dependency locking"
        fi
        ;;
esac

# 17. Environment configuration
if [ -f ".env.example" ] || [ -f ".env.template" ]; then
    check_status 0 "Environment template exists"
else
    warn_status "No environment template" "Create .env.example with required variables"
fi

echo ""
echo "🏆 FINAL SCORE"
echo "----------------------------------------"

SCORE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))

if [ $SCORE -ge 80 ]; then
    echo -e "${GREEN}🏆 EXCELLENT! Score: $SCORE% ($PASSED_CHECKS/$TOTAL_CHECKS)${NC}"
    echo -e "${GREEN}Your project follows senior development practices!${NC}"
elif [ $SCORE -ge 60 ]; then
    echo -e "${YELLOW}🥉 GOOD! Score: $SCORE% ($PASSED_CHECKS/$TOTAL_CHECKS)${NC}"
    echo -e "${YELLOW}Your project is on the right track, but has room for improvement.${NC}"
elif [ $SCORE -ge 40 ]; then
    echo -e "${YELLOW}⚠️  NEEDS WORK! Score: $SCORE% ($PASSED_CHECKS/$TOTAL_CHECKS)${NC}"
    echo -e "${YELLOW}Consider implementing more best practices.${NC}"
else
    echo -e "${RED}🔥 NEEDS MAJOR IMPROVEMENTS! Score: $SCORE% ($PASSED_CHECKS/$TOTAL_CHECKS)${NC}"
    echo -e "${RED}This project needs significant work to meet professional standards.${NC}"
fi

echo ""
echo "💡 NEXT STEPS:"
echo "----------------------------------------"
echo "1. Address failed checks (❌) first - these are critical"
echo "2. Consider warnings (⚠️) for best practices"
echo "3. Re-run this checker periodically"
echo "4. Share with team for code review standards"

echo ""
echo "🔗 USEFUL RESOURCES:"
echo "----------------------------------------"
echo "• GitHub Actions: https://docs.github.com/actions"
echo "• Docker Best Practices: https://docs.docker.com/develop/dev-best-practices/"
echo "• Security Checklist: https://owasp.org/www-project-top-ten/"
echo "• Code Quality: https://sonarqube.org/"

echo ""
echo "==============================================="
echo "✨ Project health check completed!"
echo "   Run with: ./project-health-checker.sh [path]"
echo "==============================================="