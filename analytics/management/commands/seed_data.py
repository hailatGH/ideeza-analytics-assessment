import random
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from analytics.models import Blog, BlogView, Country


class Command(BaseCommand):
    help = "Seed the database with random data for demo purposes."

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # country
        countries_data = [
            ("Ethiopia", "ET"),
            ("Israel", "IL"),
            ("United States", "US"),
            ("France", "FR"),
            ("United Kingdom", "GB"),
            ("India", "IN"),
            ("China", "CN"),
            ("Brazil", "BR"),
            ("Australia", "AU"),
            ("Italy", "IT"),
            ("Japan", "JP"),
            ("Russia", "RU"),
            ("Mexico", "MX"),
            ("South Africa", "ZA"),
            ("Spain", "ES"),
            ("Netherlands", "NL"),
            ("Sweden", "SE"),
            ("Norway", "NO"),
            ("Denmark", "DK"),
        ]

        countries = []
        for name, code in countries_data:
            country, _ = Country.objects.get_or_create(name=name, code=code)
            countries.append(country)

        # users and profiles
        users = []
        usernames = [
            "hailat",
            "eva",
            "dana",
            "eli",
            "kira",
            "mike",
            "sara",
            "tom",
            "lisa",
            "john",
            "anna",
            "mark",
            "nina",
            "paul",
            "rachel",
            "steve",
            "tina",
            "victor",
            "wendy",
            "xavier",
        ]
        for username in usernames:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password("password123")
                user.save()
                # profile is handled by signal, just update country
                user.profile.country = random.choice(countries)
                user.profile.save()
            users.append(user)

        # blogs
        now = timezone.now()
        blogs = []
        blog_topics = [
            "Django Tips",
            "Python Performance",
            "Scaling APIs",
            "Docker Secrets",
            "DB Optimization",
            "Frontend Best Practices",
            "DevOps Insights",
            "Cloud Architecture",
            "Microservices Patterns",
            "Testing Strategies",
            "Security Essentials",
            "AI in Web Development",
            "Data Science for Developers",
            "GraphQL vs REST",
            "Serverless Trends",
            "CI/CD Pipelines",
            "Code Quality Tools",
            "Open Source Contributions",
            "Tech Career Advice",
            "Remote Work Tips",
            "Tech Conferences",
        ]

        for i in range(120):
            # create blogs over the last 12 months
            days_ago = random.randint(0, 365)
            created_at = now - timedelta(days=days_ago)

            b = Blog.objects.create(
                title=f"{random.choice(blog_topics)} - Edition {i}",
                content="This is a sample blog content for analytics demo purposes only.",
                author=random.choice(users),
            )

            # need to manually set created_at since auto_now_add is True
            Blog.objects.filter(id=b.id).update(created_at=created_at)
            blogs.append(b)

        # blog views
        self.stdout.write("Generating views (this might take a moment)...")
        total_views = 0
        for blog in blogs:
            # random number of views per blog between 10 and 100
            num_views = random.randint(10, 100)
            total_views += num_views

            # views happen after the blog is created
            for _ in range(num_views):
                # views spread out from blog creation until 'now'
                creation_date = Blog.objects.get(id=blog.id).created_at
                max_delta = (now - creation_date).total_seconds()
                random_second = random.uniform(0, max_delta)
                view_time = creation_date + timedelta(seconds=random_second)

                blog_view = BlogView.objects.create(
                    blog=blog, viewer=random.choice(users)
                )
                # update timestamp manually since auto_now_add is True
                BlogView.objects.filter(id=blog_view.id).update(timestamp=view_time)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded {len(users)} users, {len(blogs)} blogs, and {total_views} views."
            )
        )
