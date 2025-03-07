from agents.export_agent import ExportAgent
import os

def generate_report():
    # Read the project report markdown file
    with open('../project_report.md', 'r') as f:
        content = f.read()
    
    # Create an export agent
    agent = ExportAgent()
    
    # Generate the PDF report
    filename = 'Deep_Research_AI_System_Report.pdf'
    filepath = agent.export_pdf(content, filename=filename)
    
    print(f'Report exported to: {os.path.abspath(filepath)}')

if __name__ == "__main__":
    generate_report() 