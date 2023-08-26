from __future__ import annotations

import time
import random
from dataclasses import dataclass

from django.core.paginator import Paginator
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django_htmx.middleware import HtmxDetails
from faker import Faker

from .forms import OddNumberForm


# Typing pattern recommended by django-stubs:
# https://github.com/typeddjango/django-stubs#how-can-i-create-a-httprequest-thats-guaranteed-to-have-an-authenticated-user
class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


@require_GET
def index(request: HtmxHttpRequest) -> HttpResponse:
    return render(request, "adamchainz/index.html")


@require_GET
def favicon(request: HtmxHttpRequest) -> HttpResponse:
    return HttpResponse(
        (
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
                + '<text y=".9em" font-size="90">🦊</text>'
                + "</svg>"
        ),
        content_type="image/svg+xml",
    )


# CSRF Demo


@require_GET
def csrf_demo(request: HtmxHttpRequest) -> HttpResponse:
    return render(request, "adamchainz/csrf-demo.html")


@require_POST
def csrf_demo_checker(request: HtmxHttpRequest) -> HttpResponse:
    form = OddNumberForm(request.POST)
    if form.is_valid():
        number = form.cleaned_data["number"]
        number_is_odd = number % 2 == 1
    else:
        number_is_odd = False
    return render(
        request,
        "adamchainz/csrf-demo-checker.html",
        {"form": form, "number_is_odd": number_is_odd},
    )


# Error demo


@require_GET
def error_demo(request: HtmxHttpRequest) -> HttpResponse:
    return render(request, "adamchainz/error-demo.html")


@require_GET
def error_demo_trigger(request: HtmxHttpRequest) -> HttpResponse:
    1 / 0
    return render(request, "adamchainz/error-demo.html")  # unreachable


# Middleware tester

# This uses two views - one to render the form, and the second to render the
# table of attributes.


@require_GET
def middleware_tester(request: HtmxHttpRequest) -> HttpResponse:
    return render(request, "adamchainz/middleware-tester.html")


@require_http_methods(["DELETE", "POST", "PUT"])
def middleware_tester_table(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request,
        "adamchainz/middleware-tester-table.html",
        {"timestamp": time.time()},
    )


# Partial rendering example


# This dataclass acts as a stand-in for a database model - the example app
# avoids having a database for simplicity.


@dataclass
class Person:
    id: int
    name: str


faker = Faker()
people = [Person(id=i, name=faker.name()) for i in range(1, 235)]


@require_GET
def partial_rendering(request: HtmxHttpRequest) -> HttpResponse:
    # Standard Django pagination
    page_num = request.GET.get("page", "1")
    page = Paginator(object_list=people, per_page=10).get_page(page_num)

    # The htmx magic - use a different, minimal base template for htmx
    # requests, allowing us to skip rendering the unchanging parts of the
    # template.
    if request.htmx:
        base_template = "adamchainz/_partial.html"
    else:
        base_template = "adamchainz/_base.html"

    return render(
        request,
        "adamchainz/partial-rendering.html",
        {
            "base_template": base_template,
            "page": page,
        },
    )


# Bud Bytes
# source https://www.youtube.com/watch?v=to1exRe7Z8E&ab_channel=BugBytes
def bb_index(request):
    print(request.htmx)
    print('Target of the swap:', request.htmx.target)
    print('Trigger of the request:', request.htmx.trigger)
    print('Boosted:', request.htmx.boosted)
    # __bool__ method allow us to use htmx object in if statement so Django new is it htmx request or not
    if request.htmx:
        print('HTMX Request :)')
        return render(request, "adamchainz/_bb_partial.html")
    else:
        print('Not HTMX Request :(')
        return render(request, "adamchainz/bb_index.html")


from django_htmx.http import HttpResponseClientRedirect


def bb_client_redirect(request):
    if request.htmx:
        return HttpResponseClientRedirect("/admin/")


from django_htmx.http import HttpResponseClientRefresh


def bb_client_refresh(request):
    if request.htmx:
        print('Trigger of the refresh request:', request.htmx.trigger)
        return HttpResponseClientRefresh()
    else:
        print('Not HTMX Request :(')
        return render(request, "adamchainz/bb_index.html")


from django_htmx.http import HttpResponseLocation, HttpResponseStopPolling


def bb_client_location(request):
    if request.htmx:
        print('Trigger of the location request:', request.htmx.trigger)
        return HttpResponseLocation("/bb-success/", target="#success-content")
    else:
        print('Not HTMX Request :(')
        return render(request, "adamchainz/bb_index.html")


def bb_success(request):
    if random.random() < 0.35:
        print('Polling terminating ...')
        return HttpResponseStopPolling()
    return HttpResponse('Congratulation - what ever you have doing worked!')


def bb_response_modyfying_functions(request: HtmxHttpRequest) -> HttpResponse:
    if request.htmx:
        return render(request, "adamchainz/_bb_push_url_in_browser_history.html")
    else:
        return render(request, "adamchainz/bb_index.html")


from django_htmx.http import push_url, reswap


def bb_push_url(request: HtmxHttpRequest) -> HttpResponse:
    if request.htmx:
        response = render(request, "adamchainz/_bb_push_url_in_browser_history.html")
        return push_url(response, "/myURL/")
    else:
        return render(request, "adamchainz/bb_index.html")


def bb_reswap(request: HtmxHttpRequest) -> HttpResponse:
    if request.htmx:
        response = render(request, "adamchainz/_bb_partial_li.html")
        return reswap(response, 'beforeend')
    else:
        return render(request, "adamchainz/bb_index.html")


from .forms import FilmForm


def bb_retarget(request):
    if request.htmx:
        form = FilmForm(request.GET)
        if form.is_valid():
            return HttpResponse("Successfully submitted form! ")
    else:
        context = {'form': FilmForm()}
        return render(request, "adamchainz/bb_index.html", context)
