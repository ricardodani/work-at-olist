from django.shortcuts import render


class BillRetrieveView(GenericAPIView):
    '''
    Get a bill API endpoint. Requires `source` and `period` GET parameters.
    If `period` is not given, then the actual period is used.
    '''

    http_method_names = ['get']
    serializer_class = BillInputSerializer

    @staticmethod
    def get_period(period):
        '''
        Return a `date` of the period or a `date` of today`s month if period is
        is None.
        Raises exception if period is invalid.
        '''
        if period:
            try:
                return datetime.strptime(period, '%Y-%m').date()
            except:
                raise exceptions.InvalidPeriodDateError
        return date.today().replace(day=1)

    def get(self, request):
        serializer = BillInputSerializer(data=self.request.GET)

        if not serializer.is_valid():
            return Response(
                dict(errors=serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )

        source = serializer.data.get('source')
        try:
            period = self.get_period(serializer.data.get('period')) # TODO: make serializer return validated period already as a date
            bill_queryset = CompletedCall.objects.get_bill(source, period)
        except APIException as e:
            return Response(
                dict(detail=e.default_detail), status=e.status_code
            )

        result_serializer = BillSerializer(dict(
            calls=bill_queryset,
            total=sum(
                call.price for call in bill_queryset if call.price
            ),
            period=period.strftime('%Y-%m'),
            source=source
        ))
        return Response(result_serializer.data)


