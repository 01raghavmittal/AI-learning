# AWS AI on Coursera — Course Notes

---

## Day 1 — Exercise: Invoking an Amazon Bedrock Foundation Model

### Overview

In this exercise, you'll use Amazon Bedrock APIs to:

- ✅ Generate videos **asynchronously** with the `start_async_invoke` API and save them to an S3 bucket.
- ✅ Create and transform text through the `invoke_model` API.
- ✅ Stream AI-generated text responses in real time using the `invoke_model_with_response_stream` API.

> ⚠️ **Note:** The exercises in this course will have an associated charge in your AWS account. Resources created: **Amazon Q Developer** and **Amazon Bedrock**.
>
> Familiarize yourself with [Amazon Q Developer pricing](https://aws.amazon.com/q/developer/pricing/), [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/), and the [AWS Free Tier](https://aws.amazon.com/free/).

---

### Troubleshooting Tips

> 🤔 If you get stuck or run into any errors, go back a few steps to ensure you didn't miss any instructions.

- 🔁 Rerun the previous cells to ensure your environment is correctly set up.
- 🧹 Restart your kernel and clear output to reset the environment.
- 📋 Double-check for typos in code or parameter names.
- 🌐 Make sure your internet connection is active (for any API calls).
- 📄 Look at the error message carefully — it often tells you exactly what's wrong.

---

### Task 1: Install Python

#### Windows

> ⚠️ If you already have Python 3 installed, you may skip this task.

1. Download the latest Python 3 from [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. Open the installer and select **"Add python.exe to PATH"**, then click **Install Now**.
3. Click **Close** to finish.
4. Verify the installation:

```bash
python3 --version
```

#### Mac

> ⚠️ If you already have Brew and Python 3 installed, you may skip this task.

1. Open Terminal and install Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Verify Homebrew:

```bash
brew --version
```

3. Install Python 3:

```bash
brew install python
```

4. Verify Python:

```bash
python3 --version
```

---

### Task 2: Install Visual Studio Code 2022

> If already installed, skip this task.

- Download from: [https://visualstudio.microsoft.com/downloads/](https://visualstudio.microsoft.com/downloads/)
- **Mac:** Expand the ZIP and drag **Visual Studio Code.app** to the Applications folder.
- **Windows:** Run the installer with default values.

---

### Task 3: Install AWS CLI

#### Windows

```powershell
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```

#### Mac

```bash
brew install awscli
```

Verify the installation:

```bash
aws --version
```

---

### Task 4: Create an AWS Account

> If you already have an AWS account for these exercises, skip this task.

1. Open the [AWS sign-up page](https://aws.amazon.com/).
2. Fill in your email address (this becomes your root user name).
3. Set an AWS account name (nickname, can be changed later).
4. Choose **Verify email address** and complete the security verification.
5. Check your email for a verification code and paste it.
6. Set and confirm your **Root user password**.
7. Fill in contact information → Billing information → Phone verification.
8. Select **Basic support - Free** and complete sign-up.
9. Click **Go to the AWS Management Console**.

---

### Task 5: Create an IAM User and Configure AWS CLI

> ⚡ Best practice: Use an IAM user instead of the root user (principle of least privilege).

#### Task 5.1: Create an IAM User

1. In the AWS Management Console, search for and open **IAM**.
2. Save the **Sign-in URL for IAM users** shown on the dashboard.
3. Navigate to **Users → Create user**.
4. Name the user: `exerciseuser`.
5. Select **"Provide user access to the AWS Management Console"**.
6. Under **"Are you providing console access to a person?"** choose **"I want to create an IAM user"**.
7. Select **Custom password** and enter a secure password. Store it safely.
8. Uncheck **"Users must create a new password at next sign-in"**.
9. Click **Next → Attach policies directly** → select **AdministratorAccess** → **Next → Create User**.
10. Open the created user → **Security credentials** tab → **Create access key**.
11. Select **Other**, add description: `Generative AI Exercises`, then **Create access keys**.
12. **Download the `.csv` file** — you will need these credentials later.

#### Task 5.2: Configure AWS CLI

1. Open Terminal and run:

```bash
aws configure
```

2. Enter your **AWS Access Key ID** and **AWS Secret Access Key** from the CSV file.
3. Set **Default region name** to `us-east-1`.
4. Set **Default output format** to `json`.
5. Verify:

```bash
aws s3 ls
```

---

### Task 6: Create a Python Environment and Install Packages

#### Task 6.1: Create the Virtual Environment

```bash
cd ~/Desktop
python3 -m venv exercise1
```

Activate it:

| OS      | Command                              |
|---------|--------------------------------------|
| Windows | `.\exercise1\Scripts\Activate.ps1`  |
| Mac     | `source exercise1/bin/activate`      |

You should see `exercise1` appear in your terminal prompt.

#### Task 6.2: Install Python Packages

```bash
pip install boto3 jupyter
```

- **boto3** — lets Python interact with AWS.
- **jupyter** — used to run code against Amazon Bedrock.

---

### Task 7: Enable Amazon Bedrock Models

1. Open the AWS Console and sign in as `exerciseuser`.
2. Ensure you are in the **us-east-1** region.
3. Search for and open **Amazon Bedrock**.
4. Select **Model access → Modify model access**.
5. Enable the following models:
   - ✅ Amazon Nova Micro
   - ✅ Amazon Nova Canvas
   - ✅ Amazon Nova Reel
6. Click **Next → Submit**.

> You should see: *"Model access updates submitted"*.

---

### Task 8: Create an S3 Bucket for Video Generation

1. Open **S3** from the AWS Console.
2. Click **Create bucket**.
3. Name it: `gen-ai-exercise-<YOUR INITIALS>` (e.g., `gen-ai-exercise-rm`).
4. Click **Create bucket**.

---

### Task 9: Generate Videos with Amazon Bedrock

1. In Terminal, start Jupyter:

```bash
jupyter notebook
```

2. Create a new notebook: **File → New → Notebook** → Select **Python 3** → Rename to `genai-exercise1-video.ipynb`.

3. Paste the following code in the first cell (replace the S3 URI with your bucket name):

```python
import boto3
import json
import random

bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")
bedrock = boto3.client(service_name="bedrock", region_name="us-east-1")
s3 = boto3.client("s3")

model_id = "amazon.nova-reel-v1:0"
prompt = "A person dancing on a mountain."

# Replace with your bucket name:
# "s3Uri": "s3://gen-ai-exercise-<YOUR INITIALS>/video/"
```

4. Run the cell. You should receive an **Invocation ARN**.

5. In a new cell, check the job status:

```python
job_status = bedrock_runtime.get_async_invoke(invocationArn=invocation_arn)
print("Current Status:", job_status["status"])
```

> ⏳ Wait 2–3 minutes. When you see `Current Status: Completed`, find the video in your S3 bucket.

---

### Task 10: Text Generation with Amazon Bedrock (`invoke_model`)

1. Create a new notebook: rename to `genai-exercise1-text1.ipynb`.
2. Paste and run the following:

```python
import boto3
import json

MODEL_ID = "amazon.nova-micro-v1:0"
bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

response = bedrock.invoke_model(
    modelId=MODEL_ID,
    guardrailVersion="DRAFT",
    body=json.dumps({
        # ... your prompt body here
    })
)
```

---

### Task 11: Streaming Text Generation (`invoke_model_with_response_stream`)

1. Create a new notebook: rename to `genai-exercise1-text2.ipynb`.
2. Paste and run the following:

```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
model_id = 'amazon.nova-micro-v1:0'

payload = {
    "messages": [
        {
            "role": "user",
            # ... your content here
        }
    ]
}
```

> The cell output will show the transformed text streamed in real time.

---

### Task 12: Cleanup

- Stop the Jupyter server by shutting down your Terminal.
- Delete the `exercise1` folder if you no longer need the environment.

---

### Summary

You now know how to:

- ✅ Launch a Jupyter Notebook to interact with Amazon Bedrock.
- ✅ Generate videos asynchronously and save them to an S3 bucket.
- ✅ Perform text generation and editing using Bedrock's `invoke_model` API.
- ✅ Stream AI-generated text responses in real time.
- ✅ Use Bedrock APIs to create and transform content efficiently.

---

### Additional Resources

- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Amazon Bedrock API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/)
- [Boto3 SDK Docs](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

---
---

## Day 2 — Amazon Q Developer

### Overview

**Amazon Q Developer** is a powerful AI-powered coding assistant that transforms how developers interact with their development environment. It combines advanced language models with deep AWS expertise to offer:

- Real-time coding suggestions
- Automated code analysis
- Interactive problem-solving right in your IDE

---

### Core Features and Capabilities

#### 💬 Intelligent Chat Interface

Powered by Amazon Bedrock, Q Developer's chat interface is your personal coding companion. You can:

- Ask technical questions about AWS services and best practices
- Request code explanations and documentation
- Generate code solutions for specific tasks
- Debug and troubleshoot issues in real-time

#### 🤖 Code Generation and Enhancement

Trained on billions of lines of code (including Amazon's internal repositories and open-source projects), Q Developer offers:

- Context-aware code suggestions as you type
- Complete function and application scaffolding
- AWS service integration templates
- Code optimization recommendations
- Security vulnerability detection and remediation

---

### Specialized AI Agents

Amazon Q Developer ships with purpose-built agents accessible from the chat interface:

| Agent | Command | Purpose |
|-------|---------|---------|
| **Development Agent** | `/dev` | Code writing, refactoring, AWS best practices |
| **Testing Agent** | `/test` | Generate test cases, identify edge cases, improve coverage |
| **Review Agent** | `/review` | Automated code reviews, coding standards, architectural improvements |
| **Transform Agent** | `/transform` | Code migration, legacy modernization, framework conversion |
| **Documentation Agent** | `/doc` | Create docs, generate API references, produce usage guides |

---

### Practical Example: Serverless Data Processing

```python
# Task: Create a Lambda function to process SQS messages

# Simply ask Q Developer:
"Create a Python Lambda function that processes messages from an SQS queue
 and stores the data in DynamoDB"

# Q Developer will generate a complete solution including:
# - Function structure
# - AWS SDK integration
# - Error handling
# - Logging
# - Best practices implementation
```

---

### Practical Example: Code Modernization (Java 8 → Java 17)

```java
// Simply ask in the chat:
"Help me upgrade this Java 8 application to Java 17. Here are the key files..."

// Q Developer will:
// 1. Analyze your codebase
// 2. Identify deprecated features
// 3. Suggest modern replacements
// 4. Guide you through breaking changes

// For instance, it might suggest:
// - Updating Collections code to use new Stream APIs
// - Replacing old DateTime code with java.time
// - Modernizing try-catch blocks with try-with-resources
```

> Amazon Q Developer breaks down complex migration tasks into manageable steps, explains the changes, and helps you implement them correctly.

---

### Common Use Cases

Developers typically use Amazon Q Developer for:

- Writing new AWS applications
- Debugging existing code
- Learning AWS services
- Implementing security best practices
- Generating documentation
- Modernizing applications

---

### Additional Resources

- [Amazon Q Developer User Guide](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/)
- [Amazon Q Detector Library](https://docs.aws.amazon.com/codeguru/detector-library/)

---
---

## Day 2 (Part 2) — Exercise: Building with Amazon Q Developer in VS Code

### Overview

In this exercise, you'll explore building with Amazon Q Developer using the **Visual Studio Code extension**. You'll start with a simple, buggy Python CLI application and use Amazon Q Developer to debug, improve, and add functionality to it.

> ✏️ **Note:** Amazon Q Developer generates **nondeterministic** output — the exact results cannot be predetermined. You may need to iterate and troubleshoot beyond what is defined here.

> ⚠️ This exercise will have an associated charge in your AWS account. Familiarize yourself with [Amazon Q Developer pricing](https://aws.amazon.com/q/developer/pricing/) and the [AWS Free Tier](https://aws.amazon.com/free/).

**You will:**

- ✅ Sign up for an AWS Builder ID
- ✅ Install and connect to Amazon Q Developer
- ✅ Explore and fix bugs in an existing Python app
- ✅ Convert the app to a basic web application using the `/dev` agent
- ✅ Generate documentation using the `/doc` agent

---

### Troubleshooting Tips

- 🔁 Rerun the application or refresh the Q Developer chat.
- 📋 Double-check for typos in code or invalid inputs.
- 🌐 Make sure your internet connection is active.
- 🧹 Restart Visual Studio Code if Q Developer isn't responding.

---

### Prerequisites

Before you start, ensure you have:

- Python 3.x
- AWS CLI configured (`aws configure`)
- Visual Studio Code

> If any of these are missing, return to Exercise 1 (Day 1) to install them.

---

### Task 1: Create an AWS Builder ID

An **AWS Builder ID** is a free personal identity that lets you access tools like Amazon Q Developer without being tied to a specific AWS account.

1. Visit the [AWS Builder ID creation guide](https://docs.aws.amazon.com/signin/latest/userguide/create-aws_builder_id.html) and follow the instructions.
2. Sign up with your email and verify your account.

---

### Task 2: Set Up the Project and Install Amazon Q Developer Extension

#### Create the Virtual Environment

**Mac:**

```bash
cd ~/Desktop && python3 -m venv exercise2 && source exercise2/bin/activate && pip install boto3 jupyter
```

**Windows:**

```powershell
cd ~/Desktop
python -m venv exercise2
.\exercise2\Scripts\Activate.ps1
pip install boto3 jupyter
```

#### Install the Extension in VS Code

1. Open **Visual Studio Code**.
2. Select **File → Open Folder** and navigate to the `exercise2` folder.
3. Go to the **Extensions** panel, search for `Amazon Q`, and install the **Amazon Q Developer** extension.
4. Click the **Q icon** in the sidebar and sign in using your **AWS Builder ID**.

---

### Task 3: Load and Explore the Python CLI App

1. Create a new folder named `code` inside your project: **File → Open Folder → New Folder → Create**.
2. Inside `code`, create a new **Python File**: **File → New File → Python File**.
3. Copy and paste the following starter code and save it as `task_tracker.py`:

```python
class Task:
    def __init__(self, name, priority):
        self.name = name
        self.priority = int(priority)

    def __str__(self):
        return f"[Priority {self.priority}] {self.name}"

class TaskManager:
    def __init__(self):
        # ... (rest of implementation)
        pass
```

4. In Terminal, navigate to the `code` folder and run:

```bash
python task_tracker.py
```

5. Try **adding**, **listing**, and **removing** tasks to explore the current behavior.

---

### Task 4: Debug with Amazon Q Developer

The app has known defects. Try these actions to uncover the bugs:

- Add a task with a **non-integer priority** (e.g., `high`).
- Remove a task with an **out-of-range index**.
- Observe **sorting behavior** when listing tasks (priority 1 = highest, 5 = lowest — notice the bug).

#### Using Q Developer Chat to Fix Bugs

In VS Code, go to **Amazon Q → Open Chat Panel** and ask:

```
Why does the app crash on non-integer input?
How to fix the error when an out-of-range task index is input for removal?
How to validate inputs?
How to sort the task list by priority in ascending order?
```

- For each question, Q Developer will identify the issue and suggest a fix.
- Review the updates and **accept** the ones you're satisfied with.
- Iterate until all defects are resolved.

---

### Task 5: Convert to Flask Web App Using the `/dev` Agent

Use the `/dev` agent to convert the CLI app into a **Flask web application**:

```
/dev Convert this CLI task tracker into a Flask web app that saves tasks to a local file.
Include a front-end and back-end implementation. Use the code folder as context.
If any dependencies are needed, generate them in the requirements.txt file in the code directory.
```

> ⏰ Q Developer will generate a plan and code — this may take a few minutes.

> 🚨 If you see *"The folder you selected is too large"*, follow the prompts to change the source folder to the `code` folder.

#### Install Dependencies and Run the App

1. Open a new Terminal in VS Code: **Terminal → New Window**.
2. Navigate to the `code` directory.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

> ✏️ If `pip` is not found, try one of these fixes:
> - **Option 1:** Use your system Terminal: `pip install -r requirements.txt`
> - **Option 2:** Use `pip3 install -r requirements.txt`
> - **Option 3:** Create and activate a virtual environment ([guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/))
> - **Option 4:** Check the [pip documentation](https://pip.pypa.io/en/stable/)

4. Start the app:

```bash
flask run
```

5. Copy the localhost URL (e.g., `http://127.0.0.1:5000/`) and open it in your browser.

> 🚨 If the app fails to run, paste the error into the Q chat and ask for a fix.

---

### Task 6: Generate Documentation Using the `/doc` Agent

1. Open a new Q chat window and type:

```
/doc
```

2. Select the option to **create a README** for your project.
3. Follow the steps provided by Q Developer.
4. Save the generated README in your project folder and review it.
5. Iterate with Q Developer until satisfied.

---

### Task 7: Cleanup

1. Stop the Flask app: press `Ctrl+C` in the Terminal.
2. Exit Amazon Q Developer by clicking the **X** button in the chat interface.

---

### Summary

You've now:

- ✅ Debugged a Python CLI app using Q Developer chat
- ✅ Fixed code issues and validated user inputs
- ✅ Converted the app into a Flask web application using `/dev`
- ✅ Generated project documentation using `/doc`
- ✅ Practiced interacting with multiple Amazon Q Developer agents

---

### Additional Resources

- [Amazon Q Developer](https://aws.amazon.com/q/developer/)
- [Amazon Q Developer User Guide](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/)
- [Amazon Q Developer for GitHub](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/amazon-q-in-github.html)
- [Amazon Q Developer on the Command Line](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-getting-started-installing.html)
