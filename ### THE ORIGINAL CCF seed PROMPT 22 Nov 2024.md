Alright, so I need to automate the content creation process using NocoDB, n8n, and Generative AI APIs. The goal is to generate daily social media content for clients, starting with text scripts based on content archetypes. Each archetype has specific prompts that guide the AI to create engaging content aligned with the client’s goals and audience.

First, I should set up the database structure in NocoDB. I need tables for clients, content themes, context premises, viral content ideas, and each content archetype like persuasive tweets, storytelling, etc. Each table should have the necessary fields, and I need to establish relationships between them, like linking content themes to clients and context premises to content themes.

Next, I need to handle the workflow automation in n8n. The process starts with uploading a CSV file containing context premises. The n8n workflow should monitor a specific Google Drive folder for new CSV uploads. Once a file is detected, it should import the data into NocoDB’s context premises table, ensuring that each premise is linked to the correct client and content theme.

After the data is in NocoDB, the system should generate viral content ideas using generative AI. For each context premise, it should create value-based and emotion-based content ideas and store them in the viral\_content\_ideas table. It should also use Perplexity AI to fetch trending insights for each idea and store that information in the same table.

Then, I need to assign content archetypes to each viral content idea based on the associated content framework. Mandatory archetypes like Persuasive Tweets and Observational Humor should be automatically selected, along with one additional archetype for diversity. Each archetype should be linked to its specific prompts from the prompts library.

Once the archetypes and prompts are assigned, the system should generate scripts for each archetype using the generative AI. These scripts should incorporate the stream of consciousness and trending insights to make them more relevant and engaging. The generated scripts should be stored in their respective content archetype tables in NocoDB.

After generating the scripts, the system should organize them into Google Docs. A new folder should be created in Google Drive for each day, and within that folder, separate documents should be created for each content archetype, containing all the scripts for that archetype.

Additionally, I need to set up image generation automation. For content archetypes that require images, like short video scripts or conceptual contrast visuals, the system should generate the necessary images using an image generation API. These images should be stored and linked to the corresponding scripts in NocoDB.

Finally, I should ensure that all the generated scripts and images are exported into CSV files that match the technical guidelines for Canva templates. This means each content archetype table should correspond to a specific Canva template, and the CSV export should include all the required fields and image assets in the correct format.

Throughout this process, I need to make sure that the workflow is fully automated, from the CSV upload to the final organization of scripts and images in Google Drive. This will streamline content creation, reduce manual effort, and ensure consistency and quality across all generated content.

Workflow for Automated Content Creation System  
1\. Database Structure in NocoDB  
Client Info Table

Client ID

Client Name

Profile Picture

Target Audience

Coach Insights

Content Themes

Language

Content Themes Table

Client ID (linked to Client Info Table)

Content Theme

SPR Text

Context Premise Table

Client ID (linked to Client Info Table)

Content Theme (linked to Content Themes Table)

DHD, Wants, Frustrations, Dreams, Fears, Suspicions, Insecurities, Envy Feelings, Enemies, Copying Mechanism

Viral Content Ideas Table

Content Idea

Client ID (linked to Client Info Table)

Context Premise (linked to Context Premise Table)

stream\_of\_consciousness

Viral Content Framework

Content Archetypes

Trending Insights

Content Archetype Tables (e.g., Persuasive Tweets, Storytelling, etc.)

Content Idea (linked to Viral Content Ideas Table)

Client ID

Context Premise

stream\_of\_consciousness

Viral Content Framework

Scripts

Prompts Library Table

Prompt Type

Content Archetype Association

Framework Association

Prompt Template

Variables Required

Short Description

Content Framework Table

content\_framework\_id

framework\_name

associated\_archetypes

2\. Workflow Automation in n8n  
Step 1: CSV Input for Context Premises

Monitor Google Drive folder for CSV uploads.

Import CSV data into Context Premise Table in NocoDB.

Link content\_theme to Content Themes Table based on client\_id.

Step 2: Generating Viral Content Ideas

Use Generative AI to create content ideas based on context premises.

Store ideas in Viral Content Ideas Table.

Use Perplexity AI to fetch trending insights and store in the same table.

Step 3: Assigning Content Archetypes and Mapping Prompts

Assign content archetypes based on content framework.

Ensure mandatory archetypes (e.g., Persuasive Tweets, Observational Humor) are selected.

Choose one additional archetype for diversity.

Map prompts from Prompts Library to each content archetype.

Step 4: Generating Scripts for Each Content Archetype

Use Generative AI to generate scripts based on selected prompts.

Incorporate stream\_of\_consciousness and trending\_insights.

Store scripts in respective content archetype tables.

Step 5: Organizing Scripts in Google Docs

Create a new folder in Google Drive for each day.

Generate Google Docs for each content archetype.

Store all scripts for a content archetype in a single document.

Organize documents in the daily folder.

3\. Image Generation Automation  
Image Generation Workflow

Identify content archetypes requiring images (e.g., short video scripts, conceptual contrast visuals).

Use an image generation API to create necessary images.

Store images and link them to corresponding scripts in NocoDB.

4\. Exporting to CSV for Canva Templates  
CSV Export Workflow

Export data from content archetype tables to CSV files.

Ensure CSV files match Canva template requirements.

Include all necessary fields and image assets in the correct format.

5\. Finalization and Output  
Automated Folder Structure

Daily folder creation in Google Drive.

Organization of Google Docs by content archetype.

Ensuring all scripts and images are neatly organized and accessible.

Technical Guidelines

Ensure content archetype tables match Canva templates.

Maintain consistency in output formats and image sizes.

This workflow automates content creation from CSV input to organized output, ensuring high-quality, engaging content aligned with client goals and audience needs.

