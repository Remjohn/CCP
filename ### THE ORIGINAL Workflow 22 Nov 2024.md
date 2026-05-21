

\#\#\# Workflow for Automated Content Creation System

\#\#\#\# 1\. Database Structure in NocoDB

\- \*\*Client Info Table\*\*  
  \- Client ID  
  \- Client Name  
  \- Profile Picture  
  \- Target Audience  
  \- Coach Insights  
  \- Content Themes  
  \- Language

\- \*\*Content Themes Table\*\*  
  \- Client ID (linked to Client Info Table)  
  \- Content Theme  
  \- SPR Text

\- \*\*Context Premise Table\*\*  
  \- Client ID (linked to Client Info Table)  
  \- Content Theme (linked to Content Themes Table)  
  \- DHD, Wants, Frustrations, Dreams, Fears, Suspicions, Insecurities, Envy Feelings, Enemies, Copying Mechanism

\- \*\*Viral Content Ideas Table\*\*  
  \- Content Idea  
  \- Client ID (linked to Client Info Table)  
  \- Context Premise (linked to Context Premise Table)  
  \- stream\_of\_consciousness  
  \- Viral Content Framework  
  \- Content Archetypes  
  \- Trending Insights

\- \*\*Content Archetype Tables\*\* (e.g., Persuasive Tweets, Storytelling, etc.)  
  \- Content Idea (linked to Viral Content Ideas Table)  
  \- Client ID  
  \- Context Premise  
  \- stream\_of\_consciousness  
  \- Viral Content Framework  
  \- Scripts

\- \*\*Prompts Library Table\*\*  
  \- Prompt Type  
  \- Content Archetype Association  
  \- Framework Association  
  \- Prompt Template  
  \- Variables Required  
  \- Short Description

\- \*\*Content Framework Table\*\*  
  \- content\_framework\_id  
  \- framework\_name  
  \- associated\_archetypes

\#\#\#\# 2\. Workflow Automation in n8n

\- \*\*Step 1: CSV Input for Context Premises\*\*  
  \- Monitor Google Drive folder for CSV uploads.  
  \- Import CSV data into Context Premise Table in NocoDB.  
  \- Link content\_theme to Content Themes Table based on client\_id.

\- \*\*Step 2: Generating Viral Content Ideas\*\*  
  \- Use Generative AI to create content ideas based on context premises.  
  \- Store ideas in Viral Content Ideas Table.  
  \- Use Perplexity AI to fetch trending insights and store in the same table.

\- \*\*Step 3: Assigning Content Archetypes and Mapping Prompts\*\*  
  \- Assign content archetypes based on content framework.  
  \- Ensure mandatory archetypes (e.g., Persuasive Tweets, Observational Humor) are selected.  
  \- Choose one additional archetype for diversity.  
  \- Map prompts from Prompts Library to each content archetype.

\- \*\*Step 4: Generating Scripts for Each Content Archetype\*\*  
  \- Use Generative AI to generate scripts based on selected prompts.  
  \- Incorporate stream\_of\_consciousness and trending\_insights.  
  \- Store scripts in respective content archetype tables.

\- \*\*Step 5: Organizing Scripts in Google Docs\*\*  
  \- Create a new folder in Google Drive for each day.  
  \- Generate Google Docs for each content archetype.  
  \- Store all scripts for a content archetype in a single document.  
  \- Organize documents in the daily folder.

\#\#\#\# 3\. Image Generation Automation

\- \*\*Image Generation Workflow\*\*  
  \- Identify content archetypes requiring images (e.g., short video scripts, conceptual contrast visuals).  
  \- Use an image generation API to create necessary images.  
  \- Store images and link them to corresponding scripts in NocoDB.

\#\#\#\# 4\. Exporting to CSV for Canva Templates

\- \*\*CSV Export Workflow\*\*  
  \- Export data from content archetype tables to CSV files.  
  \- Ensure CSV files match Canva template requirements.  
  \- Include all necessary fields and image assets in the correct format.

\#\#\#\# 5\. Finalization and Output

\- \*\*Automated Folder Structure\*\*  
  \- Daily folder creation in Google Drive.  
  \- Organization of Google Docs by content archetype.  
  \- Ensuring all scripts and images are neatly organized and accessible.

\- \*\*Technical Guidelines\*\*  
  \- Ensure content archetype tables match Canva templates.  
  \- Maintain consistency in output formats and image sizes.

This workflow automates content creation from CSV input to organized output, ensuring high-quality, engaging content aligned with client goals and audience needs.  
