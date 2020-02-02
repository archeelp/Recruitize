import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from recruitment import app, db, bcrypt, mail
from recruitment.forms import (RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm )
from recruitment.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from datetime import datetime
import PyPDF2
import recruitment.mypreprocessing as mypreprocessing
import recruitment.filter_search as filter_search
import recruitment.searchprovider as searchprovider
import random

chu = {'cs': [{'name': 'Apoorva Gokhale', 'skill': ['robotics', 'foundation', 'software', 'learning', 'data', 'software', 'intelligence', 'learning', 'microsoft', 
'learning', 'learning', 'robotics', '2018', 'learning', 'nlp', 'communication', 'software', 'design', 'web', 'learning', 'nlp', 'communication', 'software', 
'design', 'web', '2017', 'embedded', 'c', 'embedded', 'c', 'learning', 'data', 'robotics', 'robotics', 'robotics', 'sports', 'sponsorship', 'foundation', '2018', 'research', '2018', 'iit', 'organization', 'management', 'data', 'communication', 'architecture', 'data', 'storage', 'soccer', 'player', 'sports', '20', 'sports', 'sports', '20', 'sports', 'sports', '20', 'sports', 'reinforcement', 'learning', '2018', '2017', 'mumbai', '10', 'mumbai', '10', 'learning', 'web', 'application', 'classification', '2018', 'learning', 'learning', 'features', 'canvas', 'flask', 'learning', 'learning', 'features', 'canvas', 'flask', '2017', '2.0', 'pid', '2', '2.0', 'pid', '2', '2.0', 'pid', '2', '2016', 'frisbee', 'robot', 'software', 'kinect', 'encoders', 'localization', 'frisbee', 'robot', 'software', 'kinect', 'encoders', 'localization', '2016', 'robot', '2', 'pid', '40', 'robot', '2', 'pid', 'robot', '2', 'pid', '40', 'research', '1', '2', 
'1', '2', 'software', '2018', 'entrepreneurship', 'processing', '2018', 'entrepreneurship', 'processing', '2018', 'entrepreneurship', 'processing', 'linkedin', 'project', 'samsung', 'processing', 'software', 'samsung', 'advanced', 'web', 'finance', 'software', 'learning', 'linkedin', 'data', 'learning', 'research', 'data', 'data', 'analytics', 'teaching', 'texas']}, {'name': 'Kevin Jain', 'skill': ['commerce', 'ipm', 'amazon', 'linux', 'office', 'project', 'management', 'operations', '2018', '6', 'intelligence', 'gardening', 'gardening', 'internet', 'microsoft', 'css', 'arduino', 'soil', 'microsoft', 'intelligence', 'intelligence', 'gardening', 'gardening', 'internet', 'microsoft', 'css', 'arduino', 'soil', 'microsoft', 'internet', 'data', 'communication', 'learning', 'data', 'internet', 'data', 'communication', 'learning', 'data', 'mumbai', 'technology', 'design', 'fundamentals', 'data', 'software', 'architecture', 'design', 'data', 'cloud', 'data', 'mining', 'database', 'management', 'statistics', 'storage', 'web', 'computing', 'mumbai', 'technology', 'design', 'fundamentals', 'data', 'software', 'architecture', 'design', 'mumbai', 'technology', 'design', 'fundamentals', 'data', 'software', 'architecture', 'design', 'data', 'cloud', 'data', 'mining', 'database', 'management', 'statistics', 'storage', 'web', 'computing', 'commerce', 'commerce', '2015', 'public', 'public', '2016', 'data', 'organization', 'mining', 'management', 'data', 'storage', 'computing', 'architecture', 'design', '2018', 'intelligence', 'intelligence', '2018', 'gardening', '2018', 'gardening', 'internet', 'microsoft', 'embedded', 'arduino', 'soil', 'microsoft', 'gardening', 'internet', 'gardening', 'internet', 'microsoft', 'embedded', 'arduino', 'soil', 'microsoft', '2017', 'architecture', 'management', '2017', '2016', 'management', '2016', 'ipm', 'english', 'record', '2016', '2015', 'mcs', 'mcs', 'aws', 'java', 'databases', 'python', 'web', 'google', 'google', 'kubernetes', 'amazon', 'paypal', 'google', 'oracle', 'samsung', 'learning', 'software', 'data', 'java', 'linux', 'c++', 'python', 'amazon', 'aws', 'ec2', 'cs', 'digital', 'data', 'linkedin', 'amazon', 'amazon', 'paypal', 'software', 'amazon', 'cs']}, {'name': 'Simran Shah', 'skill': ['vault', 'technology', 'government', 'disney', 'operations', 'analytics', 'operations', 'analytics', 'operations', 'vault', 'technology', '2018', 'fintech', '18', 'seo', '3', 'fintech', '18', 'seo', '3', '2017', '2017', '2017', 'mumbai', '2', 'mumbai', '2', '2017', 'fmcg', 'google', 'map', 'fmcg', 'google', 'map', '2016', 'technology', 'it', 'strategy', 'it', 'project', 'cloud', 'data', 'design', 'technology', 'statistics', 'it', 'strategy', 'it', 'project', 'cloud', 'data', 'design', 'technology', 'statistics', '5', 'government', 'debate', '5', 'government', 'debate', 'web', 'cloud', 'web', 'technology', 'management', 'analytics', 'digital', 'paper', 'research', 'technology', 'government', 'technology', 'project', 'management', 'digital', 'enterprise', 'technology', 'technology', 'it', 'cygnet', 'eagle', 'security', '1', 'healthcare', 'data', 'linkedin', 'windows', 'spring', 'internships', 'data', 'analytics', 'r', 'sql', 'risk', 'analytics', 'data', 'r', 'sql', 'python', 'data', 'operations', 'data', 'bloomberg', 'analytics', 
'data', 'sas', 'google', '2017']}, {'name': 'Shubham Shah', 'skill': ['2018', '1', '2017', 'ue', 'ue', 'technology', 'data', 'data', 'linkedin', 'cs', 'stack', 'building', 'construction', 'management', 'cssgb', 'data', 'strategy', 'internships', 'software', 'accountability', 'cloud', 'learning', 'intelligence', 'project', 'linkedin', 'technology', 'java', 'data', 'campus', 'vista', 'technology']}, {'name': 'Kavita Deshmukh', 'skill': ['project', 'spring', 'computing', 'computing', 'computing', 'projects', 'spring', 'computing', 'computing', 'computing', 'box', 'project', 'computing', '2011', '4', 'computing', '2011', '4', '9', '1', '4', 'scrum', 'scrum', 'scrum', 'project', 'project', 'project', 'project', 'scrum', 'scrum', 'engineers', 'engineers', 'usability', 'usability', 'scrum', 'scrum', '2', 'linkedin', 'java', 'spring', 'computing', 'security', 'spring', 'computing', 'software', 'data', 'software', 'kanban', 'project', 'management', 'linkedin', 'projects', 'spring', 'computing', 'project', 'spring', 'computing', 'express', 'technology', 'software', 'intelligence', 'public', 'it', 'project', 'project', 'cyber', 'project', 'agile', 'project', 'management', 'project', 'project', 'telecom', 'digital', 'leadership']}, {'name': 'Naman Ambavi', 'skill': ['management', 'software', 'cloud', 'application', 'web', 'design', 'application', 'design', 'linkedin', 'wordpress', 'web', 'web', 'technology', 'management', '5', '2018', '7', '2017', '11', 'management', 'management', '2017', '11', 'web', 'digital', 'linkedin', '2', 'data', 'ibm', 'questionnaires', 'ux', 'management', 'linkedin', 'alto', 'web', 'software', 'midas', 'web', 'design', 'mobile', 'application', 'management', 'hubspot', 'silver', 'web', 'mobility', '2']}, {'name': 'Mukhtar kazi', 'skill': ['film', 'web', 'software', 'software', 'linkedin', 'electronics', 'telecom', 'mumbai', '5', '3', 'articles', 'award', 'mumbai', '2014', '7', 'security', 'security', 'film', '2018', '1', 'digital', 'digital', '2016', '2014', '6', '2012', '5', '2', '2', 'electronics', 'communications', 'electronics', 'telecommunications', 'robotics', 'electronics', 'telecommunications', 'robotics', 'electronics', 'electronics', 'electronics', 'electronics', 'angularjs', '1.x', 'angularjs', '1.x', 'bowman', 'bowman', 'angular', 'java', 'java', 'branding', 'strategy', 'hiring', 'laravel', 'php', 'shopify', 'operations', 'mumbai', 'linkedin', 'wings', 'branding', 'digital', 'research', 'research', 'digital']}], 'financial': [{'name': 'shival rajgor', 'skill': ['investments', 'wealth', 'linkedin', 'wellness', 'wealth', 'wealth', 'investors', '2018', '2', '2017', '2015', 'insurance', 'nse', 'stack', 'operations', 'ml', 'research', 'credit', 'linkedin', 'commerce', 'sme', '10', 'digital']}, {'name': 'Toshik Doomra', 'skill': ['accountants', 'accountants', 'tax', 'tax', 'linkedin', 'management', 'risk', '2018', '11', 'risk', 'risk', 'risk', '2012', '5', '2010', '5', 'retail', 'retail', '2007', 'accountants', 'accountants', 'commerce', '2016', '9', 'accountants', 'accountants', 'accountants', 'cxo', 'cxo', 'capital', 'capital', '6', 'itc', 'investors', 'lashes', 
'lashes', 'money', 'linkedin', 'accountants']}, {'name': 'Ankur Parikh', 'skill': ['algo', 'llp', 'algo', 'algo', 'algo', 'python', 'algo', 'wealth', 'linkedin', '8', 'trading', 'mumbai', 'nse', 'derivatives', 'trading', 'security', 'traders', 'data', 'algo', '2012', '9', 'focus', 'research', 'forex', 'focus', 'research', 'forex', 'algo', 'trading', 'trading', 'trading', '2009', '5', 'options', 'skills', 'options', 'skills', '2016', '2011', '24', '2011', '24', '2014', 'history', 'data', '2016', 'app', 'app', 'commodities', 'app', 'app', 'commodities', 'app', 'app', 'commodities', 'trading', '2016', 'ib', 'ib', 'trading', '2016', 'c++', '2012', 'c++', '2012', '2014', '2000', 'sql', '2000', 'sql', '2000', 'sql', '2015', '2', 'api', '2', 'api', 'java', 'api', 'history', 'windows', 'linux', '2014', 't4', 'api', '2014', '6', '7', '8', 'commodity', 't4', 'api', 'live', 't4', '6', '7', '8', 'commodity', 't4', 'api', 'live', 't4', 'strategy', 'nse', 'options', 'currency', '2014', 'strategy', 'nse', 'live', 'strategy', 'nse', 'other', 'strategy', 'nse', 'nse', '2014', 'nse', 'nse', 'live', 'nse', 'nse', 'live', 'other', 'api', '2014', 'trading', '.net', 'trading', 'trading', '.net', 'trading', 'other', 'forex', '2014', '5', '1', 'forex', 'strategy', '5', '1', 'forex', 'strategy', 'trading', '2014', 'research', 'research', 'trading', '2013', '2013', 'api', 'api', '2012', 'optimization', 'optimization', '2012', 'live', '2012', 'live', '2012', 'other', 'money', 'flow', 'money', 'flow', 'box', 'box', 'forex', 'forex', 'trading', 'trading', 'currency', 'currency', 'automation', 'automation', 'data', 'data', 'trading', 'trading', 'trading', 'strategy', 'trading', 'strategy', '8', 'linkedin', '4', 'algo', 'software', 'algo', 'algo', 'hni', 'investments', 'algo', 'funding', 'trading', 'sas', '5', 'openflow', 'linkedin', 'algo', 'python', 'algo', 'stack', 'mobile', 'microsoft', '2016']}, {'name': 'Brijesh Parnaami', 'skill': ['insurance', 'insurance', 'wealth', 'finance', 'wealth', 'management', 'technology', 'insurance', 'management', 'technology', 'wealth', 'linkedin', 'bfsi', 'llp', 'insurance', 'wealth', 'finance', 'wealth', '2017', '3', '2009', '7', 'silk', 'iso', '2008', 
'llp', 'it', 'finance', 'silk', 'silk', 'iso', '2008', 'llp', 'it', 'finance', 'retail', '2004', '2', 'retail', 'retail', '3', '8', 'construction', 'construction', 'management', 'technology', 'management', 'management', 'loan', 'sme', 'loans', 'tax', 'mumbai', 'mumbai', 'openings', 'openings', 'cxo', 'cxo', 'fintech', 'fintech', '5', 'linkedin', 'retail', 'wealth', 'revenue', 'finance', 'training', 'microsoft', 'dynamics', 'linkedin', 'insurance', 'management', 'technology', 'ecommerce', 'llp', 'anthill', 'cloud', 'cloud', 'intelligence', 'it']}, {'name': 'Rohit Pol', 'skill': ['accountants', 'accountants', 'tax', 'tax', 'linkedin', 'tax', 'tax', 'tax', 'leadership', 'justice', 'accountants', 'accountants', 'astute', 'r', '3', 'institutional', 'equities', 'automation', 'operations', 'money', 'foundations', 'linkedin', 'accountants', 'projects', 'construction', 'tax', 'blockchain']}, {'name': 'Falguni Shah', 'skill': ['management', 'management', 'management', 'management', 'wealth', 'linkedin', 'wealth', '6', 'signs', 'management', '2007', '11', 'investment', 'general', 'investment', 'welfare', 'welfare', 'investments', 'project', 'software', 'finance', 'trading', 'stocks', 'risk', 'linkedin', 'management', 'management']}, {'name': 'RAJESH DOSHI', 'skill': ['c', 'c', 'accountants', 'c', 'air', 'c', 'accountants', 'tax', 'tax', 'tax', 'linkedin', 'tax', 'tax', 'tax', 'tax', 'tax', 'cancer', 'office', 'management', 'c', '4', 'tax', 'tax', 'accountants', '6', '6', 'accountants', 'accountants', 'tax', 'tax', 'linkedin', 'productivity', 'productivity', 'mhe', 'management', 'enterprise', 'infrastructure', 'management', 'linkedin', 'c', 'air', 'c', 'accountants', 'cs', 'cs', 'r', 'c', 'llp', 'llp']}], 'android': [{'name': 'Mathieu FRANCOIS', 'skill': ['digital', 'application', 'web', 'web', 'software', 'application', 'cloud', 'android', 'application', 'software', 'linkedin', 'french', 'cms', 'film', '2018', '6', '2017', '9', 'twist', 'twist', '2018', '7', 'travel', 'planet', 'planet', 'travel', 'planet', '2017', '7', 'film', 'film', '2018', '11', '2017', '11', 'digital', '2015', '10', '2015', '3', '2014', '7', 'art', 'art', 'research', 'strategy', '2013', 'strategy', 
'2011', 'research', '2009', 'management', 'entrepreneurs', 'summit', 'partnerships', 'tennis', '2011', 'entrepreneurs', 'summit', 'partnerships', 'entrepreneurs', 'summit', 'partnerships', 'tennis', '2011', '1', '1', 'linkedin', 'retail', 'design', 'manufacturing', 'gts', 'data', 'linkedin']}, {'name': 'Mirza Ismail Baig', 'skill': ['software', 'web', 'application', 'software', 'mobile', 'application', 'android', 'software', 'application', 'linkedin', 'technology', 'software', 'google', 'azure', 'cloud', '2016', 'technology', '2015', 'application', 'database', 'cms', 'application', 'database', 'cms', '.net', 'application', 'application', 'embedded', 'application', 'app', '.net', 'application', 'access', 'access', 'app', 'app', 'app', 'app', 'racing', 'equestrian', 'application', 'application', '2014', 'cms', 'web', 'cms', 'web', 'mumbai', 'mumbai', 'data', 'spark', 'flume', 'ldap', 'kafka', 'aws', 'kerberos', 'hive', 'linux', 'software', 'microsoft', 'cards', 'operations', 'ielts', 'building', 'web', 'apps', 'dart', 'building', 'mobile', 'linkedin', 'software', 'web', 'customer', 'enterprise', 'blockchain', 'nlp', 'magento', '1', '2', 'aws', 'laravel', 'linux', 'management']}, {'name': 'Vidit Shah', 'skill': ['entrepreneurship', 'commerce', 'enterprise', 'apps', 'application', 'application', 'saas', 'android', 'web', 'software', 'application', 'software', 'linkedin', 'retail', 'mobile', 'app', 'intelligence', 'aggregation', '1', 'saas', 'mobile', 'apps', 'app', 'infosys', 'general', 'public', 'fundraising', 'general', '2016', '9', 'it', 'intelligence', 'aggregation', 'app', 'apps', 'meru', 'database', 'management', '1', '11', 'it', 'intelligence', 'aggregation', 'app', 'apps', 'it', 'intelligence', 'aggregation', 'app', 'apps', 'meru', 'database', 'management', '1', '11', 'digital', 'building', 'building', 'enterprise', 'digital', 'building', 'building', 'enterprise', '2018', 'entrepreneurship', '5', 'entrepreneurship', '2014', '8', 'entrepreneurship', '2014', 'commerce', '2012', '6', 'affiliate', 'seo', 'affiliate', 'seo', 'general', 'public', 'symphony', 'instrumental', 'digital', 'symphony', '2', 'symphony', 'instrumental', 'digital', 'symphony', '2', 'debate', 'android', 'monster', '2011', 'digital', 'digital', 'mobile', 'mobile', 'web', 'web', 'entrepreneurs', 'digital', 'coaching', 'seo', 'entrepreneurs', 'digital', 'coaching', 'seo', 'blockchain', 'blockchain', '8', 'linkedin', 'symphony', '2011', 'commerce', 'training', 'keynote', 'management', 'optimization', 'structural', 'software', 'finance', '5', 'linkedin', 'enterprise', 'apps', 'blockchain', 'it', 'technology', 'digital', 'application', 'project']}, {'name': 'Shubha Hegde', 'skill': ['software', 'application', 'android', 'linkedin', 'software', 'application', 'software', 'database', 'software', 'software', 'developers', 'developers', 'android', 'android', 'developers', 'developers', 'developers', 'developers', 'flex', 'framework', 'flex', 'framework', 'data', 'data', '6', 'android', 'app', 'n', 'n', 'recruiter', 'google', '2', 'it', 'mercedes-benz', 'llc', 'linkedin', 'software', 'mobile', 'application', 'application', 'mobile', 'application', 'android', 'app', 'application', 'application', 'trading', 'mcx', 'mobile']}, {'name': 'Biswa Singha', 'skill': ['software', 'application', 'application', 'web', 'web', 'software', 'android', 'application', 'software', 'linkedin', '5', '2017', '10', '2015', '9', 'software', '2013', '1', 
'web', '2012', 'software', '2011', '4', 'software', '2010', '3', '1', 'software', '2005', 'app', 'stack', 'data', 'node.js', 'projects', 'data', 'visualization', 'linkedin', 'cloud', 'conversant', 'app', 'digital', 'stack', 'mobile', 'apps', 'angular', 'magento', 'wordpress', 'silver']}], 'HR': [{'name': 'Rashmi Vishwakarma', 'skill': ['hiring', 'management', 'project', 'public', 'software', 'software', 'hiring', 'mumbai', 'it', 'it', '2009', '360', 'it', 'it', 'pan', 'it', 'it', 'it', 'php', 'ci', 'mumbai', 'management', 'project', 'mumbai', '2017', '10', 'hiring', '2012', '11', 'mumbai', '2009', 'it', 'it', 'it', 'it', 'mumbai', '2009', 'it', 'it', 'mumbai', '2009', 'it', 'it', 'it', 'it', 'contractors', 'contractors', 'web', 'mobile', 'web', 'mobile', 'mobile', 'apps', 'mobile', 'apps', 'security', 'security', 'asterisk', 'asterisk', 'project', 'project', '6', 'linkedin', 'recruiter', 'recruiter', 'software', 'it', 'recruiter', 'ibm', 'plus', 'interviewing', 'linkedin', 'customer', 'tax', 'nucleus', 'search']}, {'name': 'Rishav Sanghai', 'skill': ['mumbai', 'linkedin', 'oil', 'public', 'smartphone', 'smartphone', 'linkedin', 'connections', 'family', 'family', '2018', '7', '2015', '9', '2014', '2014', '2014', 'rubber', 'pyrolysis', 'technology', 'rubber', 'pyrolysis', 'technology', 'design', 'entertainment', 'design', 'entertainment', 'one', 'management', 'recruiting', 'linkedin', 'bespoke', 'sourcing', 'prime']}, {'name': 'Reshma Naik', 'skill': ['aar', 'linkedin', '10', 'insurance', 'aar', 'windows', 'management', '2014', '4', 'management', 'commerce', 'finance', 'export', 'documentation', 'linkedin', 'aar', 'management']}, {'name': 'Smita Oberoi', 'skill': ['operations', 'linkedin', '15', 'oil', 'automotive', '4', 'management', 'd', 'l&d', '2014', '11', 'oil', 'gas', 'oil', 'gas', 'oil', 'gas', '2018', '2013', '2012', '1', 'management', 'management', '2011', 'management', 'management', '2009', 'operations', '2007', '2004', '5', '8', 'linkedin', 'operations', 'payments', 'operations', 'linkedin', 'radiant', 'learning']}, {'name': 'Shalini Jadhav', 'skill': ['software', 'mumbai', 'management', 'linkedin', 'customer', 'management', 'psychology', 'mumbai', '2015', '2012', '11', '16', '16', '2003', '3', '2003', '16', 'insurance', '2003', '16', 'insurance', 'flow', 'flow', 'customer', '2000', 'forwarding', 'forwarding', 'software', 'office', 'office', 'office', 'au', 'recruiter', 'management', 'microsoft', 'dynamics', 'linkedin', 'mumbai', 'capital', 'wealth', 'credit', 'express']}, {'name': 'Ralsi Sharma', 'skill': ['general', 'management', 'management', 'technology', 'public', 'management', 'linkedin', 'management', '2017', '6', '2018', '9', 'general', '2012', '11', 'survey', 'leadership', 'survey', 'leadership', '2', '2011', '3', '2010', '2009', '4', '2005', '10', 'management', 'management', 'management', 'management', 'technology', 'public', 'skills', 'skills', 'capital', 'capital', 'management', 'management', '8', 'linkedin', 'software', 'learning', 'learning', 'recruiter', 'finance', 'edge', 'edge', 'operations', 'digital', 'operations', 'linkedin', 'management', 'beacon', 'public', 'leadership', 'management', '2', 'search', 'transformational']}], 'software-testing': [{'name': 'Shyam Tarate', 'skill': ['outsourcing', 'training', 'application', 'software', 'web', 'mobile', 'application', 'web', 'software', 'application', 'software', 'application', 'linkedin', 'customer', 'management', 'technology', 'articles', 'clover', 'infosys', '2017', '3', 'project', 'outsourcing', 'web', 'mobile', 'training', 'salesforce', 'training', 'office', '9', '7', 'project', 'outsourcing', 'web', 'mobile', 'training', 'salesforce', 'training', 'office', 'project', 'outsourcing', 'web', 'mobile', 'training', 'salesforce', 'training', 'office', '9', '7', '2015', '3', 'training', 'engineers', 'php', 'blockchain', 'engineers', 'php', 'blockchain', 'mobile', 'mobile', 'recruiting', 'recruiting', 'office', 'office', '8', 'stack', 'water', 'recruiter', 'stack', 'java', 'app', 'analytics', 'salesforce', 'css', 'linkedin', 'outsourcing', 'training', 'public', 'telematics', 'llp', 'mobile', 'apps', 'nlp', 'technology', 'trustee', 'n', 'n']}, {'name': 'Araib Bhat', 'skill': ['hiring', 'mumbai', 'application', 'application', 'web', 'web', 'software', 'software', 'cloud', 'application', 'android', 'database', 'application', 'software', 'application', 'linkedin', 'customer', 'general', 'finance', 'french', '2018', '7', '2017', '1', 'outlets', 'outlets', '2016', '7', 'code', 'code', '2015', '4', 'tender', 'tender', 'digital', 'search', 'search', 'organization', 'management', 'management', 'management', 'video', 'customer', 'management', 'linkedin', 'hiring', 'mumbai', 'operations', 'operations', 'operations', 'cables', 'datacom', 'operations', 'operations', 'strategy', 'project', 'management', 'it', 'operations', 'operations', 'crowdfunding', 'operations']}, {'name': 'Nitin J.', 'skill': ['iron', 'application', 'enterprise', 'design', 'mobile', 'application', 'software', 'saas', 'cloud', 'application', 'design', 'application', 'application', 'linkedin', '11', 'entrepreneurship', 'blockchain', 'technology', 'technology', 'it', 'management', '16', 'technology', 'maya', 'iron', 'technology', 'it', 'it', 'crm', 'technology', 'web', 'application', 'cloud', 'application', 'enterprise', 'options', 'bitcoin', '2013', '2', 'it', 'it', 'it', '2013', '2', 'it', '40', 'it', 'it', 'it', '40', 'it', 'iron', '2011', '5', 'it', 'infrastructure', 'maya', 'iron', 'it', 'seo', 'sem', 'optimization', 'it', 'it', 'infrastructure', 'maya', 'iron', 'it', 'seo', 'sem', 'optimization', 'it', 'it', '2010', '2', 'it', 'infrastructure', 'it', 'web', 'internet', 'online', 'it', 'other', 'online', 'trading', 'it', 'infrastructure', 'it', 'web', 'internet', 'online', 'it', 'infrastructure', 'it', 'web', 'internet', 'online', 'it', 'other', 'online', 'trading', '2010', 'infrastructure', '4', 'vertex', 'office', 'software', 'internet', 'infrastructure', '4', 'vertex', 'office', 'software', 'internet', 'web', 'operations', 'web', 'blockchain', 'wealth', 'management', 'liquidity', 'it', 'metro', 'linkedin', 'online', 'fox', 'training', 'training', 'hiring', 'pos', 'internet']}], 'health and fitness': [{'name': 'V K Sharma, Ph.D', 'skill': ['management', 'management', 'prime', '2016', 'commercials', '2016', 'mumbai', 'congress', 'mumbai', 'transformation', 'sfe', 'interview', '2013', 'iit', 'mumbai', '2015', 'turn', 'strategy', 'leadership', 'management', 'linkedin', 'leadership', 'leadership', 'coaching', 'leadership', 'coaching', 'management', 'leadership', '5', 'conferences', 'management', 'management', 'management', 'management', 'coaching', 'leadership', 'nlp', 'leadership', 'leadership', 'coaching', 'leadership', 'coaching', 'leadership', 'leadership', 'coaching', 'leadership', 'coaching', 'management', '2017', 'kol', 'kol', '11', '2016', 
'6', 'cluster', '3', '3', 'rpm', '5', 'cluster', '3', '3', 'rpm', '5', 'cluster', '3', '3', 'rpm', '5', '2013', '5', 'focus', '3', 'focus', '3', '10', '2011', '8', '3', '13', '1', '3', '13', '1', 'general', '2010', '2', 'operations', 'operations', '2007', '6', '4', '4', '7', '2003', '7', '2000', '10', '1', '1', '1', '5', '40', '40', '40', 'management', 'management', 'philosophy', 'nlp', '1', 'nlp', 'public', 'art', 'coaching', 'leadership', 'assessment', 'management', 'management', 'management', 'legislation', 'commerce', 'research', 'research', 'leadership', 'union', 'union', 'healthcare', 'healthcare', 'summit', 'keynote', 'keynote', 'management', 'technology', 'management', 'management', 'ci', 'mumbai', 'ci', 'mumbai', 'leadership', 'prime', '2016', 'commercials', '2016', 'mumbai', 'management', 'congress', 'mumbai', 'transformation', 'sfe', 'interview', '2013', 'iit', 'mumbai', '2015', 'management', '2018', 'management', 'licensing', 'licensing', '4', '4', 'leadership', 'leadership', 'coaching', 'coaching', 'linc', 'linc', 'digital', 'cmo', 'digital', 'cmo', '8', 'linkedin', 'general', 'devices', 'training', 'engage', 'linkedin', 'turn', 'strategy', 'leadership', 'management', 'vaccines', 'dm']}, {'name': 'Kunal Popat', 'skill': ['risk', 'insurance', 'insurance', 'risk', 'insurance', 'insurance', 'commerce', 'risk', 'insurance', 'risk', 'insurance', 'insurance', 'homeowners', 'linkedin', 'insurance', 'mumbai', 'marathon', 'risk', 'insurance', 'insurance', '2005', '11', 'commerce', 'insurance', 'insurance', 'reinsurance', 'office', 'insurance', 'insurance', 'insurance', 'mumbai', 'general', 'affinity', 'liberty', 'insurance', 'bancassurance', 'insurance', 'customer', 'operations', 'general', 'r', 'project', 'linkedin', 'risk', 'insurance', 'risk', 'insurance', 'insurance', 'insurance', 'general', 'insurance', 'technology', 'digital', 'profiles', 'distributors']}, {'name': 'Nimish Thakkar', 'skill': ['management', 'project', 'healthcare', 'linkedin', 'cancer', '1', '2', '2005', '6', '2018', '11', '2009', '2009', 'intellectual', 'intellectual', 'chemicals', 'chemicals', 'cosmetics', 'cosmetics', '8', 'healthcare', 'healthcare', 'healthcare', 'research', 'testing', 'tcf', 'cisco', 'linkedin', 'pharmaceuticals', 'health', 'pharmaceuticals', 'health']}, {'name': 'Tarun Walia', 'skill': ['healthcare', 'ema', 'management', 'keynote', 'management', 'healthcare', 'linkedin', '3', '12', '8', '10', 'pipeline', 'licensing', 'commerce', 'healthcare', '1', 'healthcare', 'ema', 'healthcare', 'ema', '2018', '5', 'data', 'intelligence', 'learning', 'data', 'intelligence', 'learning', '2017', '5', '2007', '8', 'pipeline', 'ip', 'strategy', 'licensing', 'pipeline', 'ip', 'strategy', 'licensing', '2016', '4', 'analytics', 'partnerships', 'analytics', 'partnerships', '2016', '4', 'operations', 'management', 'operations', 'management', '2014', '9', 'management', 'healthcare', 'management', 'healthcare', 'management', 'management', '2012', '7', 'management', 'out-licensing', 'healthcare', 'technology', 'management', 'out-licensing', 'healthcare', 'technology', '2011', '1', 'management', 'ci', 'intelligence', 'healthcare', 'management', 'management', 'management', 'ci', 'intelligence', 'healthcare', 'management', 'ci', 'intelligence', 'healthcare', 'management', 'management', '2009', '5', '2007', '2', 'management', '6', '10', 'healthcare', 'search', 'management', '6', '10', 'healthcare', 'management', '6', '10', 'healthcare', 'search', 'research', 'research', 'intelligence', 'projects', 'healthcare', 'inflammation', 'research', 'intelligence', 'projects', 'healthcare', 'inflammation', 'management', 'management', '2011', 'connections', 'connections', 'ci', 'ci', 'connections', 'connections', 'licensing', 'licensing', 'biotechnology', 'biotechnology', 'intelligence', 'intelligence', '8', 'linkedin', '16', '18', '1', 'search', 'leadership', 'communications', 'ema', 'ema', 'search', 'technology', 'digital', 'cs', 'finance', 'finance', 'ema', 'dynamics', 'software', 'aws', 'devops', 'automation', 'telecom', 'research', 'video', 'linkedin', 'keynote', 'healthcare', 'ema', 'healthcare', 'strategy', 'n', 'n', 'strategy', 'c', 'intelligence', 'strategy', 'healthcare', 'technology', 'design', 'data', 'analytics', 'management']}, {'name': 'Rishabh Verma', 'skill': ['entertainment', 'finance', 'l&d', 'entertainment', 'design', 'finance', 'healthcare', 'linkedin', '2015', '8', '2018', '9', 'data', 'visualization', 'analytics', 'web', 'gis', 'gis', 'gis', 'web', 'gis', 'data', 'visualization', 'analytics', 'web', 'gis', 'gis', 'gis', 'data', 'visualization', 'analytics', 'web', 'gis', 'gis', 'gis', 'web', 'gis', '2018', '6', 'nse', 'google', 'app', '3', 'connect', 'nse', 'google', 'nse', 'google', 'app', '3', 'connect', '2018', '7', 'entertainment', '2016', '1', 'entertainment', 'entertainment', '2017', '1', 'internet', 'internet', '2017', '1', 'finance', '2016', '5', '2014', '9', '7', '2015', '2014', 'l&d', '2012', 'entertainment', '2012', 'entrepreneurship', 'entrepreneurship', 'entrepreneurship', 'design', 'design', 'digital', 'web', 'intelligence', 'digital', 'web', 'digital', 'web', 'intelligence', '2018', '10', 'rights', '2018', '5', '2018', '8', 'rights', '2017', '2', 'rights', '2015', '2', 'welfare', '2005', 'investment', 'investment', 'leadership', 'it', 'operations', 'devops', 'security', 'risk', 'cloud', 'data', 'leadership', 'it', 'operations', 'devops', 'security', 'risk', 'cloud', 'data', 'investment', 'investment', '5', 'linkedin', '2', 'bloomberg', 'capital', 'capital', 'keynote', 'investment', 'capital', 'iit', 'management', 'django', 'it', 'recruiter', 'fpga', 'linkedin', 'prime', 'customer', 'management']}, {'name': 'Umang Shah', 'skill': ['insurance', 'llp', 'insurance', 'insurance', 'indemnity', 'insurance', 'liability', 'insurance', 'insurance', 'health', 'linkedin', '3', '8', 'insurance', 'llp', 'insurance', 'insurance', 'mediclaim', 'cyber', 'officers', 'liability', 'health', 'insurance', 'insurance', 'architects', 'cyber', 'insurance', 'cyber', 'insurance', 'insurance', '2016', '1', '2015', '4', '2014', '6', '2012', '2', 'research', '2011', 'research', '2011', 'investment', 'dcf', 'oil', 'capital', 'research', '2011', 'investment', 'dcf', 'research', '2011', 'investment', 'dcf', 'oil', 'capital', 'management', 'indemnity', 'insurance', 'indemnity', 'insurance', 'management', 'management', 'intelligence', 'analytics', 'intelligence', 'analytics', 'membership', 'membership', 'insurance', 'insurance', '8', 'insurance', 'general', 'insurance', 'operations', 'intelligence', 'video', 'analytics', 'gems', 'general', 'iit', 'digital', 'medidata', 'finance', 'linkedin', 'insurance', 'indemnity', 'insurance', 'liability', 'insurance', 'insurance', 'sports', 'blockchain']}, {'name': 'Vidushii Luthra', 'skill': ['linkedin', 'solar', 'digital', 'amazon', '2013', '1', 'foundation', 'karma', 'rss', 'karma', 'rss', '13', '17', 'foundation', 'foundation', 'karma', 'rss', 'karma', 'rss', '13', '17', '2017', '1', 'summit', 'mos', 'government', 'union', 'cabinet', 'mos', 'government', 'union', 'cabinet', 'linkedin', 'events', 'steel', 'finance', 'management', 'linkedin', 'ngo', 'live', 'healing', 'wellness', 'happiness', 'wellness']}, {'name': 'Jignesh Barasara', 'skill': ['research', 'healthcare', 'linkedin', 'management', 'project', 'strategy', 'management', 'intelligence', 'healthcare', 'intelligence', 'healthcare', '2015', '2012', '11', '1', '6', '2012', '2', 'sports', 'visit', 'sports', 'visit', 'bioscience', 'bioscience', 'devices', 'devices', 'health', 'health', 'health', 'health', '8', 'writer', 'search', 'editing', 'mumbai', 'design', 'linkedin', 'research', 'mentoring', 'investment', 'health', 'customer', 'funding']}, {'name': 'Pradnya Sonawane', 'skill': ['research', 'research', 'research', 'linkedin', 'research', '2008', '1', 'operations', 'packers', 'web', 'linkedin', 'research', 'alto', 'physics', 'online']}]}


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',title="Home")


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/dashboard")
def dashboard():
    return render_template('index.html', title='Dashboard')

@app.route("/profile")
def profile():
    return render_template('profile.html', title='Profile')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':    
        hashed_password = bcrypt.generate_password_hash(request.form.get('password'))
        user = User(firstname=request.form.get('firstname'),lastname=request.form.get('lastname'),email=request.form.get('email'), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user and bcrypt.check_password_hash(user.password,request.form.get('password')):
            login_user(user, remember=request.form.get('remember'))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            if request.method == 'POST':
                flash('Login failed','danger')
    return render_template('login.html', title='Login')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/displaycv", methods=['GET', 'POST'])
@login_required
def displaycv():
    if request.method == 'POST':
        text = request.form['text']
        return render_template('display.html', text=text)
    return render_template('display.html', text="")

@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    categories = ['Advocate',
 'Arts',
 'Automation Testing',
 'Blockchain',
 'Business Analyst',
 'Civil Engineer',
 'Data Science',
 'Database',
 'Dev-ops Engineer',
 'DotNet Developer',
 'ATL Developer',
 'Electrical Engineering',
 'HR',
 'Hadoop',
 'Health and Fitness',
 'Java Developer',
 'Mechanical Engineer',
 'Network Security Engineer',
 'Operations Manager',
 'PMO',
 'Python Developer',
 'SAP Developer',
 'Sales',
 'Testing',
 'Web Designing'
 ]
    if request.method == 'POST':
        if request.form['submit_button'] == "Filter":
            skillsinput = request.form.get('skills')
            filters_list = []
            for i in skillsinput.split(','):
                filters_list.extend(filter_search.searchFilter(i))
            return render_template('search.html', categories=categories, filters_list=filters_list, searchQuery=skillsinput)
        else:
            skillsinput = request.form.get('skills')
            category = request.form.get('choices-single-defaul')
            results = searchprovider.giveSearchResults(category, skillsinput)
            print(results)
            return render_template('table.html', title='Table', results=results)
    
    return render_template('search.html', categories=categories)

@app.route("/scrap",methods=['GET', 'POST'])
@login_required
def scrap():
    categories = ['Advocate',
 'Arts',
 'Automation Testing',
 'Blockchain',
 'Business Analyst',
 'Civil Engineer',
 'Data scientist',
 'Database',
 'Dev-ops Engineer',
 'DotNet Developer',
 'ATL Developer',
 'Electrical Engineering',
 'HR',
 'Hadoop',
 'Health and Fitness',
 'Java Developer',
 'Mechanical Engineer',
 'Network Security Engineer',
 'Operations Manager',
 'PMO',
 'Python Developer',
 'SAP Developer',
 'Sales',
 'Testing',
 'Web Designing','Health and fitness','financial','cs']
    if request.method == 'POST':
        cat = request.form.get('choices-single-defaul')
        print(cat)
        skillsinput = request.form.get('skills')
        filters_list = []
        for i in skillsinput.split(','):
            filters_list.extend(filter_search.searchFilter(i))
        print('filters: ', filters_list)
        if request.form['submit_button'] == 'Filter':
            return render_template('stage3.html', categories=categories, filters_list=filters_list,cat=cat, searchQuery=skillsinput)
        else:
            ip = set(filters_list)
            print(ip)
            for x in chu[cat]:
                x['score'] = len(ip.intersection(set(x['skill'])))/len(ip)
                x['score'] = random.randint(0, 10)
                x['location'] = random.choice(['Mumbai','Pune','Banglore','Chennai','Hyderabad'])
                x['randomno'] = random.randint(1, 5)
            return render_template('scrap_output.html',profiles=sorted(chu[cat], key = lambda x: x['score'], reverse=True, ))
    return render_template('stage3.html',categories=categories)

# @app.route("/scrap_output/<skillsinput>/<cat>",methods=['GET', 'POST'])
# @login_required
# def scrap_output(skillsinput,cat):
#     filters_list = []
#     print(skillsinput)
#     for i in skillsinput.split(','):
#         filters_list.extend(filter_search.searchFilter(i))
#     ip = set(filters_list)
#     print(ip)
#     for x in chu[cat]:
#         x['score'] = len(ip.intersection(set(x['skill'])))/len(ip)
#         x['location'] = random.choice(['Mumbai','Pune','Banglore','Chennai','Hyderabad'])
#     return render_template('scrap_output.html',profiles=chu[cat])



@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == "POST":
        file = request.files['uploadfile']
        
        pdfReader = PyPDF2.PdfFileReader(file)  
        
        # creating a page object 
        pageObj = pdfReader.getPage(0) 
        
        # extracting text from page 
        text = pageObj.extractText()
        f = open('./recruitment/UpdatedResumeDataSet.csv', "a")
        f.write(mypreprocessing.preprocessing(text) + ", ")
        f.write(str([text]))
        f.write('\n')
        f.close()
        flash('The resume was classified as ' + mypreprocessing.preprocessing(text) + ' Successfully','success')
    return render_template('upload.html',title='Upload')

@app.route("/table")
def table():
    cinput = "Data Science"
    sinput = "Deep Learning"
    results = searchprovider.giveSearchResults(cinput, sinput)
    return render_template('table.html',title='Table', results=results)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
