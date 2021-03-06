"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""


# from django.test import TestCase
from unittest import TestCase, main
import doctest
from pug.invest import util
import pandas as pd
np = pd.np
from scipy.optimize import minimize



class SimpleTest(TestCase):
    def test_optimal_threshold(self):
        """
        Test using scipy.optimize.minimize on a bumpy data set to find the clipping threshold
        """
        return
        t = ['2014-12-09T00:00', '2014-12-09T00:15', '2014-12-09T00:30', '2014-12-09T00:45', '2014-12-09T01:00', '2014-12-09T01:15', '2014-12-09T01:30', '2014-12-09T01:45']
        ts = pd.Series([217, 234, 235, 231, 219, 219, 231, 232], index=pd.to_datetime(t))
        thresh=234
        capacity=562.5
        util.clipped_area(ts, thresh=thresh)
        pd.DataFrame({'ts': ts, 'thresh': pd.Series(thresh*np.ones(len(ts)), index=ts.index)}).plot()

        # invest.util.clipping_params()
        ts.index = ts.index.astype(np.int64)
        costs = []
        weights = np.ones(4)

        def cost_fun(x, *args):
            thresh = x[0]
            ts, capacity, bounds, costs, weights = args
            integral = util.clipped_area(ts, thresh=thresh)
            cost = 0
            terms = np.array([(100. * (integral - capacity) / capacity) ** 2,
                              1. / (((thresh - bounds[0]) / max(bounds))**2)**0.5,
                              1. / (((thresh - bounds[1]) / max(bounds))**2)**0.5,
                              1.1 ** (integral / capacity)])
            cost = np.sum(weights * terms)
            costs += [(thresh, cost, integral)]
            return cost

        bounds = (ts.min(), ts.max())
        thresh0 = 0.4*bounds[1] + 0.6*bounds[0]
        optimum = minimize(fun=cost_fun, x0=[thresh0], bounds=[bounds], args=(ts, capacity, bounds, costs, weights))
        thresh = optimum.x[0]
        integral = util.clipped_area(ts, thresh=thresh)
        self.assertGreater(capacity, integral)
        self.assertLess((capacity-integral)/capacity, 0.01)


class InvestDocTest(TestCase):

    def test_module(self, module=None):
        if module is not None:
            failure_count, test_count = doctest.testmod(module, raise_on_error=False, verbose=True)
            msg = "Ran {0} tests in {3} and {1} passed ({2} failed)".format(test_count, test_count-failure_count, failure_count, module.__file__)
            print msg
            if failure_count:
                # print "Ignoring {0} doctest failures...".format(__file__)
                self.fail(msg)
            # return failure_count, test_count

    def test_util(self):
        self.test_module(util)

if __name__ == '__main__':
    main()