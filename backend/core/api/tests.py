from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import timedelta
from django.utils import timezone

from .models import Organization, Project, Issue, TimeLog, Profile

User = get_user_model()


class ProfileModelTest(TestCase):
    """Test Profile model and signals"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_profile_created_automatically(self):
        """Test that a Profile is created when a User is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)

    def test_profile_str_method(self):
        """Test Profile string representation"""
        self.assertEqual(str(self.user.profile), 'testuser')


class OrganizationModelTest(TestCase):
    """Test Organization model"""

    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='testpass123'
        )
        self.member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='testpass123'
        )

    def test_organization_creation(self):
        """Test basic organization creation"""
        org = Organization.objects.create(name='Test Org', owner=self.owner)
        self.assertEqual(org.name, 'Test Org')
        self.assertEqual(org.owner, self.owner)
        self.assertEqual(str(org), 'Test Org')

    def test_organization_with_members(self):
        """Test organization with members"""
        org = Organization.objects.create(name='Test Org', owner=self.owner)
        org.members.add(self.member)

        self.assertIn(self.member, org.members.all())
        self.assertIn(self.owner, org.members.all())  # Owner should be included


class ProjectModelTest(TestCase):
    """Test Project model including hierarchy"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.org = Organization.objects.create(name='Test Org', owner=self.user)

    def test_project_creation_user_owner(self):
        """Test project creation with user owner"""
        project = Project.objects.create(
            name='Test Project',
            description='A test project',
            user_owner=self.user
        )
        self.assertEqual(project.name, 'Test Project')
        self.assertEqual(project.user_owner, self.user)
        self.assertIsNone(project.org_owner)
        self.assertEqual(str(project), 'Test Project')

    def test_project_creation_org_owner(self):
        """Test project creation with organization owner"""
        project = Project.objects.create(
            name='Org Project',
            description='Organization project',
            org_owner=self.org
        )
        self.assertEqual(project.org_owner, self.org)
        self.assertIsNone(project.user_owner)

    def test_project_validation_both_owners(self):
        """Test that project cannot have both user and org owners"""
        with self.assertRaises(Exception):  # Should raise ValidationError
            project = Project(
                name='Invalid Project',
                user_owner=self.user,
                org_owner=self.org
            )
            project.full_clean()

    def test_project_validation_no_owner(self):
        """Test that project must have either user or org owner"""
        with self.assertRaises(Exception):  # Should raise ValidationError
            project = Project(name='Invalid Project')
            project.full_clean()

    def test_project_hierarchy(self):
        """Test parent/child project relationships"""
        parent = Project.objects.create(
            name='Parent Project',
            user_owner=self.user
        )
        child = Project.objects.create(
            name='Child Project',
            user_owner=self.user,
            parent=parent
        )

        self.assertEqual(child.parent, parent)
        self.assertIn(child, parent.subprojects.all())

    def test_project_self_parent_validation(self):
        """Test that project cannot be its own parent"""
        project = Project.objects.create(
            name='Test Project',
            user_owner=self.user
        )

        with self.assertRaises(Exception):  # Should raise ValidationError
            project.parent = project
            project.full_clean()

    def test_project_get_descendants(self):
        """Test getting project descendants"""
        parent = Project.objects.create(
            name='Parent',
            user_owner=self.user
        )
        child1 = Project.objects.create(
            name='Child 1',
            user_owner=self.user,
            parent=parent
        )
        grandchild = Project.objects.create(
            name='Grandchild',
            user_owner=self.user,
            parent=child1
        )

        descendants = parent.get_descendants()
        self.assertIn(child1, descendants)
        self.assertIn(grandchild, descendants)
        self.assertEqual(len(descendants), 2)


class IssueModelTest(TestCase):
    """Test Issue model including hierarchy"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.project = Project.objects.create(
            name='Test Project',
            user_owner=self.user
        )

    def test_issue_creation(self):
        """Test basic issue creation"""
        issue = Issue.objects.create(
            title='Test Issue',
            description='A test issue',
            project=self.project,
            owner=self.user,
            priority=1,
            status='todo'
        )

        self.assertEqual(issue.title, 'Test Issue')
        self.assertEqual(issue.project, self.project)
        self.assertEqual(issue.owner, self.user)
        self.assertEqual(issue.priority, 1)
        self.assertEqual(issue.status, 'todo')
        self.assertEqual(str(issue), 'Test Issue')

    def test_issue_hierarchy(self):
        """Test parent/child issue relationships"""
        parent_issue = Issue.objects.create(
            title='Parent Issue',
            project=self.project,
            owner=self.user
        )
        child_issue = Issue.objects.create(
            title='Child Issue',
            project=self.project,
            owner=self.user,
            parent=parent_issue
        )

        self.assertEqual(child_issue.parent, parent_issue)
        self.assertIn(child_issue, parent_issue.subissues.all())

    def test_issue_self_parent_validation(self):
        """Test that issue cannot be its own parent"""
        issue = Issue.objects.create(
            title='Test Issue',
            project=self.project,
            owner=self.user
        )

        with self.assertRaises(Exception):  # Should raise ValidationError
            issue.parent = issue
            issue.full_clean()

    def test_issue_wrong_project_parent_validation(self):
        """Test that parent issue must be in same project"""
        other_project = Project.objects.create(
            name='Other Project',
            user_owner=self.user
        )
        parent_issue = Issue.objects.create(
            title='Parent Issue',
            project=other_project,
            owner=self.user
        )

        with self.assertRaises(Exception):  # Should raise ValidationError
            child_issue = Issue(
                title='Child Issue',
                project=self.project,
                owner=self.user,
                parent=parent_issue
            )
            child_issue.full_clean()

    def test_issue_get_descendants(self):
        """Test getting issue descendants"""
        parent = Issue.objects.create(
            title='Parent',
            project=self.project,
            owner=self.user
        )
        child1 = Issue.objects.create(
            title='Child 1',
            project=self.project,
            owner=self.user,
            parent=parent
        )
        grandchild = Issue.objects.create(
            title='Grandchild',
            project=self.project,
            owner=self.user,
            parent=child1
        )

        descendants = parent.get_descendants()
        self.assertIn(child1, descendants)
        self.assertIn(grandchild, descendants)
        self.assertEqual(len(descendants), 2)


class TimeLogModelTest(TestCase):
    """Test TimeLog model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.project = Project.objects.create(
            name='Test Project',
            user_owner=self.user
        )
        self.issue = Issue.objects.create(
            title='Test Issue',
            project=self.project,
            owner=self.user
        )

    def test_timelog_creation(self):
        """Test basic timelog creation"""
        start_time = timezone.now()
        end_time = start_time + timedelta(hours=1)

        timelog = TimeLog.objects.create(
            issue=self.issue,
            user=self.user,
            start_time=start_time,
            end_time=end_time
        )

        self.assertEqual(timelog.issue, self.issue)
        self.assertEqual(timelog.user, self.user)
        self.assertEqual(timelog.start_time, start_time)
        self.assertEqual(timelog.end_time, end_time)
        self.assertFalse(timelog.distracted)

    def test_timelog_duration(self):
        """Test timelog duration calculation"""
        start_time = timezone.now()
        end_time = start_time + timedelta(minutes=90)  # 1.5 hours

        timelog = TimeLog.objects.create(
            issue=self.issue,
            user=self.user,
            start_time=start_time,
            end_time=end_time
        )

        self.assertEqual(timelog.duration(), 90)  # 90 minutes

    def test_timelog_duration_no_end_time(self):
        """Test timelog duration when end_time is None"""
        start_time = timezone.now()

        timelog = TimeLog.objects.create(
            issue=self.issue,
            user=self.user,
            start_time=start_time,
            end_time=None
        )

        self.assertIsNone(timelog.duration())


class OrganizationAPITest(APITestCase):
    """Test Organization API endpoints"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_list_organizations(self):
        """Test listing organizations"""
        org1 = Organization.objects.create(name='Org 1', owner=self.user)
        org2 = Organization.objects.create(name='Org 2', owner=self.other_user)

        response = self.client.get(reverse('organization-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should only see own org
        self.assertEqual(response.data[0]['name'], 'Org 1')

    def test_create_organization(self):
        """Test creating an organization"""
        data = {'name': 'New Organization'}
        response = self.client.post(reverse('organization-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Organization')
        self.assertEqual(response.data['owner'], self.user.id)

    def test_organization_membership(self):
        """Test organization membership filtering"""
        org = Organization.objects.create(name='Test Org', owner=self.user)
        org.members.add(self.other_user)

        # Other user should see the org they're a member of
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(reverse('organization-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ProjectAPITest(APITestCase):
    """Test Project API endpoints"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.org = Organization.objects.create(name='Test Org', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_list_projects(self):
        """Test listing projects"""
        project1 = Project.objects.create(name='Project 1', user_owner=self.user)
        project2 = Project.objects.create(name='Project 2', org_owner=self.org)
        project3 = Project.objects.create(name='Project 3', user_owner=self.other_user)

        response = self.client.get(reverse('project-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should see own projects and org projects

    def test_create_project_user_owner(self):
        """Test creating a project with user owner"""
        data = {
            'name': 'New Project',
            'description': 'A new project',
            'user_owner': self.user.id
        }
        response = self.client.post(reverse('project-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Project')

    def test_create_project_org_owner(self):
        """Test creating a project with org owner"""
        data = {
            'name': 'Org Project',
            'description': 'Organization project',
            'org_owner': self.org.id
        }
        response = self.client.post(reverse('project-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['org_owner'], self.org.id)


class IssueAPITest(APITestCase):
    """Test Issue API endpoints"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.project = Project.objects.create(name='Test Project', user_owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_list_issues(self):
        """Test listing issues"""
        issue1 = Issue.objects.create(
            title='Issue 1',
            project=self.project,
            owner=self.user
        )
        issue2 = Issue.objects.create(
            title='Issue 2',
            project=self.project,
            owner=self.user
        )

        response = self.client.get(reverse('issue-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_issue(self):
        """Test creating an issue"""
        data = {
            'title': 'New Issue',
            'description': 'A new issue',
            'project': self.project.id,
            'priority': 1,
            'status': 'todo'
        }
        response = self.client.post(reverse('issue-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Issue')
        self.assertEqual(response.data['owner'], self.user.id)

    def test_update_issue_priority(self):
        """Test updating issue priority (Eisenhower matrix)"""
        issue = Issue.objects.create(
            title='Test Issue',
            project=self.project,
            owner=self.user,
            priority=1
        )

        data = {'priority': 2}
        response = self.client.patch(reverse('issue-detail', kwargs={'pk': issue.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['priority'], 2)


class TimeLogAPITest(APITestCase):
    """Test TimeLog API endpoints"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.project = Project.objects.create(name='Test Project', user_owner=self.user)
        self.issue = Issue.objects.create(
            title='Test Issue',
            project=self.project,
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_list_timelogs(self):
        """Test listing time logs (should only see own logs)"""
        start_time = timezone.now()

        # Create logs for both users
        TimeLog.objects.create(
            issue=self.issue,
            user=self.user,
            start_time=start_time,
            end_time=start_time + timedelta(hours=1)
        )
        other_issue = Issue.objects.create(
            title='Other Issue',
            project=self.project,
            owner=self.other_user
        )
        TimeLog.objects.create(
            issue=other_issue,
            user=self.other_user,
            start_time=start_time,
            end_time=start_time + timedelta(hours=1)
        )

        response = self.client.get(reverse('timelog-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should only see own logs

    def test_create_timelog(self):
        """Test creating a time log"""
        start_time = timezone.now()
        end_time = start_time + timedelta(hours=1)

        data = {
            'issue': self.issue.id,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat()
        }
        response = self.client.post(reverse('timelog-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.id)


class ProjectReportAPITest(APITestCase):
    """Test Project Report API endpoints"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.project = Project.objects.create(name='Test Project', user_owner=self.user)
        self.issue1 = Issue.objects.create(
            title='Issue 1',
            project=self.project,
            owner=self.user
        )
        self.issue2 = Issue.objects.create(
            title='Issue 2',
            project=self.project,
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_get_project_report(self):
        """Test getting project report with time calculations"""
        start_time = timezone.now()

        # Create some time logs
        TimeLog.objects.create(
            issue=self.issue1,
            user=self.user,
            start_time=start_time,
            end_time=start_time + timedelta(hours=2)
        )
        TimeLog.objects.create(
            issue=self.issue2,
            user=self.user,
            start_time=start_time,
            end_time=start_time + timedelta(hours=1)
        )

        response = self.client.get(
            reverse('reports-get-report', kwargs={'pk': self.project.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_time_spent', response.data)
        self.assertIn('time_per_issue', response.data)

    def test_project_report_not_found(self):
        """Test project report with non-existent project"""
        response = self.client.get(
            reverse('reports-get-report', kwargs={'pk': 999})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PermissionTest(APITestCase):
    """Test permissions and access control"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access protected endpoints"""
        response = self.client.get(reverse('organization-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_access(self):
        """Test that authenticated users can access protected endpoints"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('organization-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_data_isolation(self):
        """Test that users can only see their own data"""
        # Create data for both users
        org1 = Organization.objects.create(name='Org 1', owner=self.user)
        org2 = Organization.objects.create(name='Org 2', owner=self.other_user)

        project1 = Project.objects.create(name='Project 1', user_owner=self.user)
        project2 = Project.objects.create(name='Project 2', user_owner=self.other_user)

        # Test with user 1
        self.client.force_authenticate(user=self.user)
        org_response = self.client.get(reverse('organization-list'))
        project_response = self.client.get(reverse('project-list'))

        self.assertEqual(len(org_response.data), 1)
        self.assertEqual(len(project_response.data), 1)
        self.assertEqual(org_response.data[0]['name'], 'Org 1')
        self.assertEqual(project_response.data[0]['name'], 'Project 1')
